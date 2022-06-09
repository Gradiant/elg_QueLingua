# QueLingua
QueLingua is a tool that receives a text as an input and recognizes its language. 

This repository contains a dockerized API built over QueLingua for integrate it into the ELG. Its original code can 
be found [here](https://github.com/gamallo/QueLingua).


## Install
Instructions to execute the tool:

```
sh docker-build.sh
```

## Execute
```
docker run --rm -p 0.0.0.0:8866:8866 --name quelingua elg_quelingua:1.0
```

## Use

- For sending a JSON: 
   - Predicting the language:
   ```
   curl -X POST  http://0.0.0.0:8866/predict_json -H 'Content-Type: application/json' -d '{"type": "text", "content":"This is a default text in English language"}'
   ```
   - Predicting the language variant:
   ```
   curl -X POST  http://0.0.0.0:8866/predict_json -H 'Content-Type: application/json' -d '{"type": "text", "params":{"variant":"True"}, "content":"Dale pibe andate al boliche que estamos conversando en argentino"}'
   ```
  
- For sending a file named `file.json`:
   ```
   curl -H "Content-Type: application/json" --data @file.json http://0.0.0.0:8866/predict_json
   ```

# Test
In the folder `test` you have the files for testing the API according to the ELG specifications.
It uses an API that acts as a proxy with your dockerized API that checks both the requests and the responses.
For this follow the instructions:
1) Configure the .env file with the data of the image and your API
2) Launch the test: `docker-compose up`
3) Make the requests, instead of to your API's endpoint, to the test's endpoint:
   ```
      curl -X POST  http://0.0.0.0:8866/processText/service -H 'Content-Type: application/json' -d '{"type": "text", "content":"This is a default text in English language"}'
   ```
4) If your request and the API's response is compliance with the ELG API, you will receive the response.
   1) If the request is incorrect: Probably you will don't have a response and the test tool will not show any message in logs.
   2) If the response is incorrect: You will see in the logs that the request is proxied to your API, that it answers, but the test tool does not accept that response. You must analyze the logs.

## Known Issues:

1) [SOLVED] Crashed with texts containing some symbols such us `"` and `'`.

    - Solution for JSON mode consists of correctly represent the symbols in the request:
        - Single quote should be represented as `'\''`. 
        - Double quote should be represented as `\"`.
        - Other symbols as slashes should be also properly represented (e.g. `\\`).
    - In file mode:
        - Symbols such as quotes are manually slashed in "replace space" of `run_quelingua()` method of serve.py. 
          If any other symbol causes errors, add the correspondent replace instruction here. 


## Citation
The original work of this tool is:
- https://github.com/gamallo/QueLingua
