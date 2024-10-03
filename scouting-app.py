import sys
from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
from data import matches
from datetime import datetime


app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)


@app.route("/")
def home():
  return render_template("home.html", user_data={})


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def registration():
    return render_template("registration.html")


@app.route("/manage")
def management():
    return render_template("manage.html")


@app.route("/scoutingdash")
def scoutingdashboard():
    return render_template("scouting_dash.html")


@app.route("/drivedash")
def drivedashboard():
    return render_template("drive_dash.html")


@app.route("/form/list")
def list_forms():
    return render_template("form_list.html", submissions=[])


@app.route("/match", methods=['GET'])
def new_form():
    return render_template("match.html")


@app.route("/match", methods=["POST"])
def save_match():

  form = request.form

  matches.add({
    "scouter_name": form.get("scouter_name")
  })

  return render_template("match.html")


@socketio.on('live reload')
def handle_live_reload(message):
    log(message)


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp + ": " + message)
    sys.stdout.flush()


socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True, use_reloader=False)
