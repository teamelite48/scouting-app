#!/bin/bash

SCRIPT_PATH=$(dirname `which $0`)

function open_ui {

  wget -q -O /dev/null "http://localhost:5000" 2>&1 >/dev/null

  while true; do
    if [[ $? -eq 0 ]]; then
      # google-chrome "http://localhost:5000"
      firefox "http://localhost:5000"
      break
    else
      sleep 1
    fi
  done
}

cd $SCRIPT_PATH

cd docker
sudo docker compose up -d
cd ..

mongodb-compass &
open_ui &
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
code . &

cd docker
sudo docker compose logs -f
sudo docker compose down