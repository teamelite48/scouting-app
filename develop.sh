#!/bin/bash

function try_open_app {

  wget -q -O /dev/null "http://localhost:5000" 2>&1 >/dev/null

  if [[ $? -eq 0 ]]; then
    google-chrome "http://localhost:5000"
  else
    sleep 1
    try_open_app
  fi
}

cd docker
sudo docker compose up -d
cd ..

mongodb-compass &
try_open_app &
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
code . &

cd docker
sudo docker compose logs -f
sudo docker compose down