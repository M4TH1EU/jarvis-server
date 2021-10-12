#!/usr/bin/env bash
set -e


cd /jarvis/

if [ $ENV_STATUS = "testing" ]; then 
  git pull origin master
fi

python3 -m pip install -r requirements.txt
python3 run.py
