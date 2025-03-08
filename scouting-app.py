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
        "scouter_name": "",
        "team": "",
        "starting_position": "Not There",
        "left_start": "No",
        "algae_intake": "Does not pick up Algae",
        "coral_intake": "Does not pick up Coral",
        "start_hang": 0,
        "stop_hang": 0,
        "end_status": "Not Parked",
        "comments": "",
        "options": get_form_options()
    }



    return render_template("2025_form.html", vm=vm, bag=get_bag())

@app.route("/form/2025/new", methods=["POST"])
@login_required
def save_2025_form():
  form = request.form
  totalcoralscore = int(form.get("teleop_L1_score") or 0) + int(form.get("teleop_L2_score") or 0) + int(form.get("teleop_L3_score") or 0) + int(form.get("teleop_L4_score") or 0)
  totalcoralshots = int(totalcoralscore) + int(form.get("teleop_coral_misses") or 0)
  totalalgaeshots = int(form.get("teleop_algae_score") or 0) + int(form.get("teleop_algae_misses") or 0)
  totalprocessorshots = int(form.get("teleop_processed") or 0) + int(form.get("teleop_processor_misses") or 0)
  totalhumanshots = int(form.get("human_score") or 0) + int(form.get("human_misses") or 0)
  teleop_coral_accuracy = totalcoralscore / totalcoralshots if totalcoralshots != 0 else 0
  teleop_algae_accuracy = int(form.get("teleop_algae_score")) / totalalgaeshots if totalalgaeshots != 0 else 0
  teleop_processor_accuracy = int(form.get("teleop_processed")) / totalprocessorshots if totalprocessorshots != 0 else 0
  human_accuracy = int(form.get("human_score")) / totalhumanshots if totalhumanshots != 0 else 0
  climb_speed = int(form.get("start_hang")) - int(form.get("stop_hang"))
  created_on = str(datetime.datetime.now())
  forms.add({
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "scouter_name": form.get("scouter_name"),
    "teleop_coral_accuracy": f"{teleop_coral_accuracy:.1%}",
    "teleop_algae_accuracy": f"{teleop_algae_accuracy:.1%}",
    "teleop_processor_accuracy": f"{teleop_processor_accuracy:.1%}",
    "human_accuracy": f"{human_accuracy:.1%}",
    "climb_speed": climb_speed,
    "algae_intake": form.get("algae_intake"),
    "coral_intake": form.get("coral_intake"),
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
    "auto_coral_misses": form.get("auto_coral_misses"),
    "teleop_algae_score": form.get("teleop_algae_score"),
    "teleop_algae_misses": form.get("teleop_algae_misses"),
    "teleop_processed": form.get("teleop_processed"),
    "teleop_processor_misses" :form.get("teleop_processor_misses"),
    "teleop_L1_score": form.get("teleop_L1_score"),
    "teleop_L2_score": form.get("teleop_L2_score"),
    "teleop_L3_score": form.get("teleop_L3_score"),
    "teleop_L4_score": form.get("teleop_L4_score"),
    "teleop_coral_misses": form.get("teleop_coral_misses"),
    "human_score": form.get("human_score"),
    "human_misses": form.get("human_misses"),
    "start_hang": form.get("start_hang"),
    "stop_hang": form.get("stop_hang"),
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
    "scouter_name": form.get("scouter_name"),
    "starting_position": form.get("starting_position"),
    "algae_intake": form.get("algae_intake"),
    "coral_intake": form.get("coral_intake"),
    "left_start": form.get("left_start"),
    "auto_algae_score": form.get("auto_algae_score"),
    "auto_algae_misses": form.get("auto_algae_misses"),
    "auto_processed": form.get("auto_processed"),
    "auto_processor_misses" :form.get("auto_processor_misses"),
    "auto_L1_score": form.get("auto_L1_score"),
    "auto_L2_score": form.get("auto_L2_score"),
    "auto_L3_score": form.get("auto_L3_score"),
    "auto_L4_score": form.get("auto_L4_score"),
    "auto_coral_misses": form.get("auto_coral_misses"),
    "teleop_algae_score": form.get("teleop_algae_score"),
    "teleop_algae_misses": form.get("teleop_algae_misses"),
    "teleop_processed": form.get("teleop_processed"),
    "teleop_processor_misses" :form.get("teleop_processor_misses"),
    "teleop_L1_score": form.get("teleop_L1_score"),
    "teleop_L2_score": form.get("teleop_L2_score"),
    "teleop_L3_score": form.get("teleop_L3_score"),
    "teleop_L4_score": form.get("teleop_L4_score"),
    "teleop_coral_misses": form.get("teleop_coral_misses"),
    "human_score": form.get("human_score"),
    "human_misses": form.get("human_misses"),
    "start_hang": form.get("start_hang"),
    "stop_hang": form.get("stop_hang"),
    "end_status": form.get("end_status"),
    "comments": form.get("comments"),
    "options": get_form_options()
    }

    return render_template("2025_form.html", vm=vm, bag=get_bag())

@app.route("/form/2025/<id>", methods=["POST"])
@login_required
def update_2025_form(id):
  
  form = request.form
  totalcoralscore = int(form.get("teleop_L1_score") or 0) + int(form.get("teleop_L2_score") or 0) + int(form.get("teleop_L3_score") or 0) + int(form.get("teleop_L4_score") or 0)
  totalcoralshots = int(totalcoralscore) + int(form.get("teleop_coral_misses") or 0)
  totalalgaeshots = int(form.get("teleop_algae_score") or 0) + int(form.get("teleop_algae_misses") or 0)
  totalprocessorshots = int(form.get("teleop_processed") or 0) + int(form.get("teleop_processor_misses") or 0)
  totalhumanshots = int(form.get("human_score") or 0) + int(form.get("human_misses") or 0)
  teleop_coral_accuracy = totalcoralscore / totalcoralshots if totalcoralshots != 0 else 0
  teleop_algae_accuracy = int(form.get("teleop_algae_score")) / totalalgaeshots if totalalgaeshots != 0 else 0
  teleop_processor_accuracy = int(form.get("teleop_processed")) / totalprocessorshots if totalprocessorshots != 0 else 0
  human_accuracy = int(form.get("human_score")) / totalhumanshots if totalhumanshots != 0 else 0
  climb_speed = int(form.get("start_hang")) - int(form.get("stop_hang"))
  created_on = str(datetime.datetime.now())
  forms.update(id, {
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "scouter_name": form.get("scouter_name"),
    "teleop_coral_accuracy": f"{teleop_coral_accuracy:.1%}",
    "teleop_algae_accuracy": f"{teleop_algae_accuracy:.1%}",
    "teleop_processor_accuracy": f"{teleop_processor_accuracy:.1%}",
    "human_accuracy": f"{human_accuracy:.1%}",
    "climb_speed": climb_speed,
    "starting_position": form.get("starting_position"),
    "algae_intake": form.get("algae_intake"),
    "coral_intake": form.get("coral_intake"),
    "left_start": form.get("left_start"),
    "auto_algae_score": form.get("auto_algae_score"),
    "auto_algae_misses": form.get("auto_algae_misses"),
    "auto_processed": form.get("auto_processed"),
    "auto_processor_misses" :form.get("auto_processor_misses"),
    "auto_L1_score": form.get("auto_L1_score"),
    "auto_L2_score": form.get("auto_L2_score"),
    "auto_L3_score": form.get("auto_L3_score"),
    "auto_L4_score": form.get("auto_L4_score"),
    "auto_coral_misses": form.get("auto_coral_misses"),
    "teleop_algae_score": form.get("teleop_algae_score"),
    "teleop_algae_misses": form.get("teleop_algae_misses"),
    "teleop_processed": form.get("teleop_processed"),
    "teleop_processor_misses" :form.get("teleop_processor_misses"),
    "teleop_L1_score": form.get("teleop_L1_score"),
    "teleop_L2_score": form.get("teleop_L2_score"),
    "teleop_L3_score": form.get("teleop_L3_score"),
    "teleop_L4_score": form.get("teleop_L4_score"),
    "teleop_coral_misses": form.get("teleop_coral_misses"),
    "human_score": form.get("human_score"),
    "human_misses": form.get("human_misses"),
    "start_hang": form.get("start_hang"),
    "stop_hang": form.get("stop_hang"),
    "end_status": form.get("end_status"),
    "comments": form.get("comments"),
    "updated_by": current_user.username,
    "updated_on": created_on,
  })

  return redirect("/data")

@app.route("/form/qual/new", methods=['GET'])
@login_required
def new_super_scouting_form():

    vm = {
        "match_number": "",
        "scouter_name": "",
        "comments": "",
        "options": get_form_options()
    }



    return render_template("super_scouting.html", vm=vm, bag=get_bag())

@app.route("/form/qual/new", methods=["POST"])
@login_required
def save_super_scouting_form():
  form = request.form
  created_on = str(datetime.datetime.now())
  forms.add({
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "scouter_name": form.get("scouter_name"),
    "comments": form.get("comments"),
    "created_by": current_user.username,
    "updated_by": current_user.username,
    "created_on": created_on,
    "updated_on": created_on,
    })

  return redirect("/scouting_dashboard")

@app.route("/form/qual/<id>", methods=['GET'])
@login_required
def load_super_scouting_form(id):

    form = forms.get(id)

    vm = {
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "scouter_name": form.get("scouter_name"),
    "comments": form.get("comments"),
    "options": get_form_options()
    }

    return render_template("super_scouting.html", vm=vm, bag=get_bag())

@app.route("/form/qual/<id>", methods=["POST"])
@login_required
def update_super_scouting_form(id):
  
  form = request.form
  created_on = str(datetime.datetime.now())
  forms.update(id, {
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "scouter_name": form.get("scouter_name"),
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
