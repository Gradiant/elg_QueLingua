FROM ubuntu:18.04

RUN apt-get update -y \
	&& apt-get install -y python3-pip python3-dev \
	&& apt-get install -y wget \
	&& apt-get install -y unzip \
	&& rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN pip3 install flask flask_json

ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8"

EXPOSE 8866

RUN mkdir -p QueLingua
WORKDIR /QueLingua/

RUN wget https://api.github.com/repos/gamallo/QueLingua/zipball/master \
	&& unzip master
RUN mkdir -p /QueLingua/files/

WORKDIR ./gamallo-QueLingua-10cc405
RUN chmod -R 777 ./*
RUN . ./install_quelingua.sh

WORKDIR /QueLingua
COPY ./ /QueLingua/
CMD ["python3", "serve.py"]

