FROM python:3.12

WORKDIR /app
COPY ../ .

# COPY ../requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

# ENTRYPOINT [ "pymon scouting-app.py" ]
# ENTRYPOINT ["pip", "list"]
