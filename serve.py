import os
import subprocess

from flask import Flask, request
from flask_json import FlaskJSON, JsonError, as_json
from werkzeug.utils import secure_filename

from utils import langs, varieties

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
APP_ROOT = "./"
app.config["APPLICATION_ROOT"] = APP_ROOT
app.config["UPLOAD_FOLDER"] = "files/"
app.config["JSON_ADD_STATUS"] = False

json_app = FlaskJSON(app)

langs_and_vars = langs.copy()
langs_and_vars.update(varieties)


@as_json
@app.route("/predict_json", methods=["POST"])
def predict_json():

    data = request.get_json()
    if data["type"] != "text":
        # Standard message code for unsupported response type
        return generate_failure_response(
            status=400,
            code="elg.request.type.unsupported",
            text="Request type {0} not supported by this service",
            params=[data["type"]],
            detail=None,
        )

    if "content" not in data:
        return invalid_request_error(
            None,
        )

    elif "params" in data:
        params = data.get("params")
        variant = (
            True
            if ("variant" in params and str(params["variant"]).lower() == "true")
            else False
        )
    else:
        variant = False

    content = data["content"]

    if len(str(content)) < 5:
        return generate_failure_response(
            status=400,
            code="elg.request.type.unsupported",
            text="Request text is too short.",
            params=None,
            detail=None,
        )
    else:
        try:
            predictions = run_quelingua(str(content), variant)
            output = generate_successful_response(content, predictions)
            return output
        except Exception as e:
            text = "Unexpected error."
            # Standard message for internal error - the real error message goes in params
            return generate_failure_response(
                status=500,
                code="elg.service.internalError",
                text="Internal error during processing: {0}",
                params=[text],
                detail=e.__str__(),
            )


@json_app.invalid_json_error
def invalid_request_error(e):
    """Generates a valid ELG "failure" response if the request cannot be parsed"""
    raise JsonError(
        status_=400,
        failure={
            "errors": [{"code": "elg.request.invalid", "text": "Invalid request"}]
        },
    )


def generate_successful_response(text, language):
    response = {"type": "classification", "classes": [{"class": language}]}
    output = {"response": response}
    return output


def generate_failure_response(status, code, text, params, detail):
    error = {}
    if code:
        error["code"] = code
    if text:
        error["text"] = text
    if params:
        error["params"] = params
    if detail:
        error["detail"] = {"message": detail}

    raise JsonError(status_=status, failure={"errors": [error]})


def run_quelingua(txt, variant):
    """Runs the quelingua tool and gets the output"""

    path_quelingua = "/QueLingua/gamallo-QueLingua-10cc405/quelingua"

    txt_formatted = txt.replace('"', '\\"').replace("'", "\\'")
    command = 'echo "' + str(txt_formatted) + '" | ' + path_quelingua
    if variant:
        command += " -var"

    output = str(subprocess.check_output(command, shell=True))
    output = output.replace("b'", "").replace("\\n'", "").replace("'", "")

    return langs_and_vars[output]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8866)
