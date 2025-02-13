import bcrypt
import flask
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_socketio import SocketIO
from config import CONFIG
from data import forms
from data import teams
from data import users
from utils.log import log
import datetime
import pprint
import sys
from operator import itemgetter


login_manager = LoginManager()

app = Flask(__name__)
app.debug = CONFIG.DEBUG
app.secret_key = CONFIG.SECRET_KEY

login_manager.init_app(app)
login_manager.login_view = "login"


def get_form_options():
    return {
        "teams": list(map(lambda team: team["name"], teams.getAll())),
        "starting_position": [
            "Not There",
            "Left Side",
            "Middle",
            "Coral Station Side"
        ],
        "left_start": [
            "No",
            "Yes",
            "Attempted"
        ],
        "coral_intake": [
            "Does not pick up Coral",
            "From the Ground",
            "From the Coral Station",
            "Both"
        ],
        "algae_intake": [
            "Does not pick up Algae",
            "From the Ground",
            "From the Reef",
            "Both"
        ],
        "end_status": [
            "Not Parked",
            "Parked",
            "Cage Attempted",
            "On Cage",
            "Hung with 1 Robot",
            "Hung with 2 Robots"
        ]
    }

@login_manager.user_loader
def load_user(username):

    user = users.find(username)

    if (user.authenticated == False):
        return None

    return user


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/data", methods=["GET"])
def match_data():

    sorted_forms = sorted(forms.getAll(), key=itemgetter("created_on"), reverse=True)

    return render_template("match_data.html", forms=sorted_forms, bag=get_bag() )


@app.route("/login", methods=["POST"])
def login():

    user = users.find(request.form.get("username"))

    formBytes = request.form.get("password").encode("UTF-8")
    userBytes = user.password.encode("UTF-8")

    if (bcrypt.checkpw(formBytes, userBytes)):
        user.authenticated = True
        users.save(user)
        login_user(user)
        # next = flask.request.args.get("next")
        # return flask.redirect(next or '/scouting-dashboard')
        return redirect('/scouting_dashboard')

    return render_template("/login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():

    user = users.find(current_user.username)
    user.authenticated = False
    users.save(user)

    logout_user()

    return redirect("/")


@app.route("/")
@login_required
def home_page():
  return redirect("/scouting_dashboard")


def get_bag():
    return {
        "current_user": current_user.username
    }

@app.route("/form/2025/new", methods=['GET'])
@login_required
def new_2025_form():

    vm = {
        "match_number": "",
        "starting_position": "Not There",
        "algae_intake": 1,
        "coral_intake": 1,
        "start_hang": 0,
        "stop_hang": 0,
        "end_status": 1,
        "comments": "",
        "options": get_form_options()
    }



    return render_template("2025_form.html", vm=vm, bag=get_bag())

@app.route("/form/2025/new", methods=["POST"])
@login_required
def save_2025_form():

  form = request.form
  created_on = str(datetime.datetime.now())
  forms.add({
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "starting_position": form.get("starting_position"),
    "left_start": form.get("left_start"),
    "auto_algae_score": form.get("auto_algae_score"),
    "auto_algae_misses": form.get("auto_algae_misses"),
    "auto_processed": form.get("auto_processed"),
    "auto_processor_misses" :form.get("auto_processor_misses"),
    "auto_L1_score": form.get("auto_L1_score"),
    "auto_L2_score": form.get("auto_L2_score"),
    "auto_L3_score": form.get("auto_L3_score"),
    "auto_L4_score": form.get("auto_L4_score"),
    "auto_coral_misses,": form.get("auto_coral_misses"),
    "teleop_algae_score": form.get("teleop_algae_score"),
    "teleop_algae_misses": form.get("teleop_algae_misses"),
    "teleop_processed": form.get("teleop_processed"),
    "teleop_processor_misses" :form.get("teleop_processor_misses"),
    "teleop_L1_score": form.get("teleop_L1_score"),
    "teleop_L2_score": form.get("teleop_L2_score"),
    "teleop_L3_score": form.get("teleop_L3_score"),
    "teleop_L4_score": form.get("teleop_L4_score"),
    "teleop_coral_misses,": form.get("teleop_coral_misses"),
    "human_score": form.get("human_score"),
    "human_misses": form.get("human_misses"),
    "start_hang": form.get("start_hang"),
    "stop_hang": form.get("stop_hang"),
    "trap_score": form.get("trap_score"),
    "end_status": form.get("end_status"),
    "comments": form.get("comments"),
    "created_by": current_user.username,
    "updated_by": current_user.username,
    "created_on": created_on,
    "updated_on": created_on,
    })

  return redirect("/scouting_dashboard")

@app.route("/form/2025/<id>", methods=['GET'])
@login_required
def load_2025_form(id):

    form = forms.get(id)

    vm = {
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "starting_position": form.get("starting_position"),
    "left_start": form.get("left_start"),
    "auto_algae_score": form.get("auto_algae_score"),
    "auto_algae_misses": form.get("auto_algae_misses"),
    "auto_processed": form.get("auto_processed"),
    "auto_processor_misses" :form.get("auto_processor_misses"),
    "auto_L1_score": form.get("auto_L1_score"),
    "auto_L2_score": form.get("auto_L2_score"),
    "auto_L3_score": form.get("auto_L3_score"),
    "auto_L4_score": form.get("auto_L4_score"),
    "auto_coral_misses,": form.get("auto_coral_misses"),
    "teleop_algae_score": form.get("teleop_algae_score"),
    "teleop_algae_misses": form.get("teleop_algae_misses"),
    "teleop_processed": form.get("teleop_processed"),
    "teleop_processor_misses" :form.get("teleop_processor_misses"),
    "teleop_L1_score": form.get("teleop_L1_score"),
    "teleop_L2_score": form.get("teleop_L2_score"),
    "teleop_L3_score": form.get("teleop_L3_score"),
    "teleop_L4_score": form.get("teleop_L4_score"),
    "teleop_coral_misses,": form.get("teleop_coral_misses"),
    "human_score": form.get("human_score"),
    "human_misses": form.get("human_misses"),
    "start_hang": form.get("start_hang"),
    "stop_hang": form.get("stop_hang"),
    "trap_score": form.get("trap_score"),
    "end_status": form.get("end_status"),
    "comments": form.get("comments"),
    "created_by": current_user.username,
    "updated_by": current_user.username,
    "created_on": created_on,
    "updated_on": created_on,
    "options": get_form_options()
    }

    return render_template("2025_form.html", vm=vm, bag=get_bag())

@app.route("/form/2025/<id>", methods=["POST"])
@login_required
def update_2025_form(id):

  form = request.form


  forms.update(id, {
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "starting_position": form.get("starting_position"),
    "left_start": form.get("left_start"),
    "auto_algae_score": form.get("auto_algae_score"),
    "auto_algae_misses": form.get("auto_algae_misses"),
    "auto_processed": form.get("auto_processed"),
    "auto_processor_misses" :form.get("auto_processor_misses"),
    "auto_L1_score": form.get("auto_L1_score"),
    "auto_L2_score": form.get("auto_L2_score"),
    "auto_L3_score": form.get("auto_L3_score"),
    "auto_L4_score": form.get("auto_L4_score"),
    "auto_coral_misses,": form.get("auto_coral_misses"),
    "teleop_algae_score": form.get("teleop_algae_score"),
    "teleop_algae_misses": form.get("teleop_algae_misses"),
    "teleop_processed": form.get("teleop_processed"),
    "teleop_processor_misses" :form.get("teleop_processor_misses"),
    "teleop_L1_score": form.get("teleop_L1_score"),
    "teleop_L2_score": form.get("teleop_L2_score"),
    "teleop_L3_score": form.get("teleop_L3_score"),
    "teleop_L4_score": form.get("teleop_L4_score"),
    "teleop_coral_misses,": form.get("teleop_coral_misses"),
    "human_score": form.get("human_score"),
    "human_misses": form.get("human_misses"),
    "start_hang": form.get("start_hang"),
    "stop_hang": form.get("stop_hang"),
    "trap_score": form.get("trap_score"),
    "end_status": form.get("end_status"),
    "comments": form.get("comments"),
    "updated_by": current_user.username,
    "updated_on": created_on,
  })

  return redirect("/data")


@app.route("/scouting_dashboard", methods=["GET"])
def scouting_dashboard():


    return render_template("scouting_dashboard.html", bag=get_bag())

if CONFIG.PROD == False:

    socketio = SocketIO(app)

    @socketio.on('live reload')
    def handle_live_reload(message):
        log(message)


    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True, use_reloader=False)