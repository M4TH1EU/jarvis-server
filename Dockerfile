FROM ubuntu:21.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ENV_STATUS=${NODE_ENV:-production}

# For suport set local time zone.
RUN apt-get update -y && apt-get upgrade -y

WORKDIR /jarvis

RUN apt install python3.9 python3-pip python3.9-dev python3.9-distutils python3-fann2 libfann-dev swig git python3-levenshtein curl -y

RUN git clone --branch $(curl --silent "https://api.github.com/repos/m4th1eu/jarvis-server/releases/latest" | grep -Po '"tag_name": "\K.*?(?=")') --progress --verbose https://github.com/M4TH1EU/jarvis-server.git .

RUN python3 -m pip install -r requirements.txt

RUN apt-get clean -y

EXPOSE 5000

COPY start.sh /jarvis/

RUN chmod +x start.sh

CMD "./start.sh"