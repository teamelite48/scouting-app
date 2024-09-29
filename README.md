# 🔍 Scouting App

## ✅ Requirements

- [Python 3.12](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com) or [Docker Engine](https://docs.docker.com/engine/install/)
- [Compass](https://www.mongodb.com/products/tools/compass)

## 🚀 Getting Started

### macOS/Linux

1. Run `./develop.sh`

###  Windows

#### Create an Environment

```
> py -3 -m venv .venv
```

#### Activate Environment

````
> .venv\Scripts\activate
````

#### Install Requirements
```
> pip install -r requirements.txt
```

#### Start Application Server
1. Run `docker compose up` from docker directory
1. Open: [localhost:5000](http://localhost:5000)

#### Stop Application Server

1. Stop server: `CTRL+C`
1. Stop containers: `docker compose down`

## 🧑‍🔬 Test Local MongoDB Connection

### macOS/Linux
1. Run `python3 mongodb_test.py`

### Windows
1. Run `py -3 mongodb_test.py`

## 📝 How to Generate requirements.txt
Creates a text file named `requirements.txt` listing installed Python packages and their versions.
```
pip freeze > requirements.txt
```