# THIS IS ONLY A TEST, NOT READY FOR PRODUCTION

FROM ubuntu:21.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /jarvis-server

RUN apt update && apt upgrade -y

RUN apt install python3.9 python3-pip python3.9-dev python3.9-distutils python3-fann2 libfann-dev swig git python3-levenshtein -y

RUN git clone  --progress --verbose https://github.com/M4TH1EU/jarvis-server.git .

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3", "run.py"]