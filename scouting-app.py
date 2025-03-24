import bcrypt
import flask
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_socketio import SocketIO
from config import CONFIG
from data import forms
from data import quals
from data import pits
from data import teams
from data import users
from utils.log import log
import datetime
import pprint
import sys
from operator import itemgetter


login_manager = LoginManager()

app = Flask(__name__)
# Existing imports and code

# Add a custom filter to check if a value is numeric
# def is_number(value):
#     try:
#         float(value)
#         return True
#     except ValueError:
#         return False

# app.jinja_env.filters['is_number'] = is_number
app.debug = CONFIG.DEBUG
app.secret_key = CONFIG.SECRET_KEY

login_manager.init_app(app)
login_manager.login_view = "login"

@app.before_request
def require_login():
    if not current_user.is_authenticated and request.endpoint not in ['login', 'login_page', 'static']:
        return redirect('/login')


def get_form_options():
    return {
        "team": list(map(lambda team: team["name"], teams.getAll())),
        "match_number": [
            "Practice",
            "Qualification 1",
            "Qualification 2",
            "Qualification 3",
            "Qualification 4",
            "Qualification 5",
            "Qualification 6",
            "Qualification 7",
            "Qualification 8",
            "Qualification 9",
            "Qualification 10",
            "Qualification 11",
            "Qualification 12",
            "Qualification 13",
            "Qualification 14",
            "Qualification 15",
            "Qualification 16",
            "Qualification 17",
            "Qualification 18",
            "Qualification 19",
            "Qualification 20",
            "Qualification 21",
            "Qualification 22",
            "Qualification 23",
            "Qualification 24",
            "Qualification 25",
            "Qualification 26",
            "Qualification 27",
            "Qualification 28",
            "Qualification 29",
            "Qualification 30",
            "Qualification 31",
            "Qualification 32",
            "Qualification 33",
            "Qualification 34",
            "Qualification 35",
            "Qualification 36",
            "Qualification 37",
            "Qualification 38",
            "Qualification 39",
            "Qualification 40",
            "Qualification 41",
            "Qualification 42",
            "Qualification 43",
            "Qualification 44",
            "Qualification 45",
            "Qualification 46",
            "Qualification 47",
            "Qualification 48",
            "Qualification 49",
            "Qualification 50",
            "Qualification 51",
            "Qualification 52",
            "Qualification 53",
            "Qualification 54",
            "Qualification 55",
            "Qualification 56",
            "Qualification 57",
            "Qualification 58",
            "Qualification 59",
            "Qualification 60",
            "Qualification 61",
            "Qualification 62",
            "Qualification 63",
            "Qualification 64",
            "Qualification 65",
            "Qualification 66",
            "Qualification 67",
            "Qualification 68",
            "Qualification 69",
            "Qualification 70",
            "Qualification 71",
            "Qualification 72",
            "Qualification 73",
            "Qualification 74",
            "Qualification 75",
            "Qualification 76",
            "Qualification 77",
            "Qualification 78",
            "Qualification 79",
            "Qualification 80",
            "Qualification 81",
            "Qualification 82",
            "Qualification 83",
            "Qualification 84",
            "Qualification 85",
            "Qualification 86",
            "Qualification 87",
            "Qualification 88",
            "Qualification 89",
            "Qualification 90",
            "Qualification 91",
            "Qualification 92",
            "Qualification 93",
            "Qualification 94",
            "Qualification 95",
            "Qualification 96",
            "Qualification 97",
            "Qualification 98",
            "Qualification 99",
            "Qualification 100",
        ],
        "starting_position": [
            "Not There",
            "Left Coral Side",
            "Middle of Reef",
            "Processor Side"
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
            "Shallow Cage",
            "Deep Cage"
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

def get_teams():
    return {
        "team": list(map(lambda team: team["name"], teams.getAll())),
    }

@app.route("/data", methods=["GET"])
def match_data():

    vm = {
        "team": "",
        "options": get_teams()
    }

    sorted_forms = sorted(forms.getAll(), key=itemgetter("created_on"), reverse=True)

    sorted_quals = sorted(quals.getAll(), key=itemgetter("created_on"), reverse=True)

    sorted_pits = sorted(pits.getAll(), key=itemgetter("created_on"), reverse=True)

    return render_template("match_data.html", vm=vm, pits=sorted_pits, quals=sorted_quals, forms=sorted_forms, bag=get_bag() )

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
        "auto_algae_score": 0,
        "auto_algae_misses": 0,
        "auto_processed": 0,
        "auto_processor_misses": 0,
        "auto_L1_score": 0,
        "auto_L2_score": 0,
        "auto_L3_score": 0,
        "auto_L4_score": 0,
        "auto_coral_misses": 0,
        "teleop_algae_score": 0,
        "teleop_algae_misses": 0,
        "teleop_processed": 0,
        "teleop_processor_misses": 0,
        "teleop_L1_score": 0,
        "teleop_L2_score": 0,
        "teleop_L3_score": 0,
        "teleop_L4_score": 0,
        "teleop_coral_misses": 0,
        "algae_intake": "Does not pick up Algae",
        "coral_intake": "Does not pick up Coral",
        "end_status": "Not Parked",
        "comments": "",
        "options": get_form_options()
    }



    return render_template("2025_form.html", vm=vm, bag=get_bag())

@app.route("/form/2025/new", methods=["POST"])
@login_required
def save_2025_form():
  form = request.form
  total_teleop_coral_score = int(form.get("teleop_L1_score") or 0) + int(form.get("teleop_L2_score") or 0) + int(form.get("teleop_L3_score") or 0) + int(form.get("teleop_L4_score") or 0)
  total_teleop_coral_shots = int(total_teleop_coral_score) + int(form.get("teleop_coral_misses") or 0)
  total_teleop_algae_shots = int(form.get("teleop_algae_score") or 0) + int(form.get("teleop_algae_misses") or 0)
  total_teleop_processor_shots = int(form.get("teleop_processed") or 0) + int(form.get("teleop_processor_misses") or 0)
  teleop_coral_accuracy = total_teleop_coral_score / total_teleop_coral_shots if total_teleop_coral_shots != 0 else 0
  teleop_algae_accuracy = int(form.get("teleop_algae_score")) / total_teleop_algae_shots if total_teleop_algae_shots != 0 else 0
  teleop_processor_accuracy = int(form.get("teleop_processed")) / total_teleop_processor_shots if total_teleop_processor_shots != 0 else 0
  totalautocoralscore = int(form.get("auto_L1_score") or 0) + int(form.get("auto_L2_score") or 0) + int(form.get("auto_L3_score") or 0) + int(form.get("auto_L4_score") or 0)
  total_coral_score = totalautocoralscore + total_teleop_coral_score
  total_algae_score = int(form.get("auto_algae_score") or 0) + int(form.get("teleop_algae_score") or 0)
  total_processed = int(form.get("auto_processed") or 0) + int(form.get("teleop_processed") or 0)
  created_on = str(datetime.datetime.now())
  forms.add({
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "scouter_name": form.get("scouter_name"),
    "teleop_coral_accuracy": f"{teleop_coral_accuracy:.1%}",
    "teleop_algae_accuracy": f"{teleop_algae_accuracy:.1%}",
    "teleop_processor_accuracy": f"{teleop_processor_accuracy:.1%}",
    "total_coral_score": total_coral_score,
    "total_algae_score": total_algae_score,
    "total_processed": total_processed,
    "algae_intake": form.get("algae_intake"),
    "coral_intake": form.get("coral_intake"),
    "starting_position": form.get("starting_position"),
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
    "end_status": form.get("end_status"),
    "comments": form.get("comments"),
    "options": get_form_options()
    }

    return render_template("2025_form.html", vm=vm, bag=get_bag())

@app.route("/form/2025/<id>", methods=["POST"])
@login_required
def update_2025_form(id):
  
  form = request.form
  total_teleop_coral_score = int(form.get("teleop_L1_score") or 0) + int(form.get("teleop_L2_score") or 0) + int(form.get("teleop_L3_score") or 0) + int(form.get("teleop_L4_score") or 0)
  total_teleop_coral_shots = int(total_teleop_coral_score) + int(form.get("teleop_coral_misses") or 0)
  total_teleop_algae_shots = int(form.get("teleop_algae_score") or 0) + int(form.get("teleop_algae_misses") or 0)
  total_teleop_processor_shots = int(form.get("teleop_processed") or 0) + int(form.get("teleop_processor_misses") or 0)
  teleop_coral_accuracy = total_teleop_coral_score / total_teleop_coral_shots if total_teleop_coral_shots != 0 else 0
  teleop_algae_accuracy = int(form.get("teleop_algae_score")) / total_teleop_algae_shots if total_teleop_algae_shots != 0 else 0
  teleop_processor_accuracy = int(form.get("teleop_processed")) / total_teleop_processor_shots if total_teleop_processor_shots != 0 else 0
  totalautocoralscore = int(form.get("auto_L1_score") or 0) + int(form.get("auto_L2_score") or 0) + int(form.get("auto_L3_score") or 0) + int(form.get("auto_L4_score") or 0)
  total_coral_score = totalautocoralscore + total_teleop_coral_score
  total_algae_score = int(form.get("auto_algae_score") or 0) + int(form.get("teleop_algae_score") or 0)
  total_processed = int(form.get("auto_processed") or 0) + int(form.get("teleop_processed") or 0)
  created_on = str(datetime.datetime.now())
  forms.update(id, {
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "scouter_name": form.get("scouter_name"),
    "teleop_coral_accuracy": f"{teleop_coral_accuracy:.1%}",
    "teleop_algae_accuracy": f"{teleop_algae_accuracy:.1%}",
    "teleop_processor_accuracy": f"{teleop_processor_accuracy:.1%}",
    "total_coral_score": total_coral_score,
    "total_algae_score": total_algae_score,
    "total_processed": total_processed,
    "starting_position": form.get("starting_position"),
    "algae_intake": form.get("algae_intake"),
    "coral_intake": form.get("coral_intake"),
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
    "end_status": form.get("end_status"),
    "comments": form.get("comments"),
    "updated_by": current_user.username,
    "updated_on": created_on,
  })

  return redirect("/data")

def get_qual_options():
    return {
        "match_number": [
            "Practice",
            "Qualification 1",
            "Qualification 2",
            "Qualification 3",
            "Qualification 4",
            "Qualification 5",
            "Qualification 6",
            "Qualification 7",
            "Qualification 8",
            "Qualification 9",
            "Qualification 10",
            "Qualification 11",
            "Qualification 12",
            "Qualification 13",
            "Qualification 14",
            "Qualification 15",
            "Qualification 16",
            "Qualification 17",
            "Qualification 18",
            "Qualification 19",
            "Qualification 20",
            "Qualification 21",
            "Qualification 22",
            "Qualification 23",
            "Qualification 24",
            "Qualification 25",
            "Qualification 26",
            "Qualification 27",
            "Qualification 28",
            "Qualification 29",
            "Qualification 30",
            "Qualification 31",
            "Qualification 32",
            "Qualification 33",
            "Qualification 34",
            "Qualification 35",
            "Qualification 36",
            "Qualification 37",
            "Qualification 38",
            "Qualification 39",
            "Qualification 40",
            "Qualification 41",
            "Qualification 42",
            "Qualification 43",
            "Qualification 44",
            "Qualification 45",
            "Qualification 46",
            "Qualification 47",
            "Qualification 48",
            "Qualification 49",
            "Qualification 50",
            "Qualification 51",
            "Qualification 52",
            "Qualification 53",
            "Qualification 54",
            "Qualification 55",
            "Qualification 56",
            "Qualification 57",
            "Qualification 58",
            "Qualification 59",
            "Qualification 60",
            "Qualification 61",
            "Qualification 62",
            "Qualification 63",
            "Qualification 64",
            "Qualification 65",
            "Qualification 66",
            "Qualification 67",
            "Qualification 68",
            "Qualification 69",
            "Qualification 70",
            "Qualification 71",
            "Qualification 72",
            "Qualification 73",
            "Qualification 74",
            "Qualification 75",
            "Qualification 76",
            "Qualification 77",
            "Qualification 78",
            "Qualification 79",
            "Qualification 80",
            "Qualification 81",
            "Qualification 82",
            "Qualification 83",
            "Qualification 84",
            "Qualification 85",
            "Qualification 86",
            "Qualification 87",
            "Qualification 88",
            "Qualification 89",
            "Qualification 90",
            "Qualification 91",
            "Qualification 92",
            "Qualification 93",
            "Qualification 94",
            "Qualification 95",
            "Qualification 96",
            "Qualification 97",
            "Qualification 98",
            "Qualification 99",
            "Qualification 100",
        ],
        "team": list(map(lambda team: team["name"], teams.getAll()))
    }

@app.route("/form/qual/new", methods=['GET'])
@login_required
def new_super_scouting_form():

    vm = {
        "scouter_name": "",
        "comments": "",
        "options": get_qual_options()
    }



    return render_template("super_scouting_form.html", vm=vm, bag=get_bag())

@app.route("/form/qual/new", methods=["POST"])
@login_required
def save_super_scouting_form():
  form = request.form
  created_on = str(datetime.datetime.now())
  quals.add({
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

    form = quals.get(id)

    vm = {
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "scouter_name": form.get("scouter_name"),
    "comments": form.get("comments"),
    "options": get_qual_options()
    }

    return render_template("super_scouting_form.html", vm=vm, bag=get_bag())

@app.route("/form/qual/<id>", methods=["POST"])
@login_required
def update_super_scouting_form(id):
  
  form = request.form
  created_on = str(datetime.datetime.now())
  quals.update(id, {
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "scouter_name": form.get("scouter_name"),
    "comments": form.get("comments"),
    "updated_by": current_user.username,
    "updated_on": created_on,
  })

  return redirect("/data")

def get_pit_options():
    return {
        "team": list(map(lambda team: team["name"], teams.getAll())),
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
        ]
    }

@app.route("/form/pit/new", methods=['GET'])
@login_required
def new_pit_form():

    vm = {
        "scouter_name": "",
        "team": "",
        "base": "",
        "dimensions": "",
        "weight": "",
        "algae_intake": "Does not pick up Algae",
        "coral_intake": "Does not pick up Coral",
        "auto_best_score": 0,
        "comments": "",
        "options": get_pit_options()
    }



    return render_template("pit_form.html", vm=vm, bag=get_bag())

@app.route("/form/pit/new", methods=["POST"])
@login_required
def save_pit_form():
  form = request.form
  created_on = str(datetime.datetime.now())
  pits.add({
    # "photos": form.get("photos"),
    "scouter_name": form.get("scouter_name"),
    "team": form.get("team"),
    "base": form.get("base"),
    "dimensions": form.get("dimensions"),
    "weight": form.get("weight"),
    "algae_intake": form.get("algae_intake"),
    "coral_intake": form.get("coral_intake"),
    "L4": form.get("L4"),
    "L3": form.get("L3"),
    "L2": form.get("L2"),
    "L1": form.get("L1"),
    "auto_move": form.get("auto_move"),
    "auto_score": form.get("auto_score"),
    "auto_best_score": form.get("auto_best_score"),
    "shallow": form.get("shallow"),
    "deep": form.get("deep"),
    "comments": form.get("comments"),
    "created_by": current_user.username,
    "updated_by": current_user.username,
    "created_on": created_on,
    "updated_on": created_on,
    })

  return redirect("/scouting_dashboard")

@app.route("/form/pit/<id>", methods=['GET'])
@login_required
def load_pit_form(id):

    form = pits.get(id)

    vm = {
    # "photos": form.get("photos"),
    "scouter_name": form.get("scouter_name"),
    "team": form.get("team"),
    "base": form.get("base"),
    "dimensions": form.get("dimensions"),
    "weight": form.get("weight"),
    "algae_intake": form.get("algae_intake"),
    "coral_intake": form.get("coral_intake"),
    "L4": form.get("L4"),
    "L3": form.get("L3"),
    "L2": form.get("L2"),
    "L1": form.get("L1"),
    "auto_move": form.get("auto_move"),
    "auto_score": form.get("auto_score"),
    "auto_best_score": form.get("auto_best_score"),
    "shallow": form.get("shallow"),
    "deep": form.get("deep"),
    "comments": form.get("comments"),
    "options": get_form_options()
    }

    return render_template("pit_form.html", vm=vm, bag=get_bag())

@app.route("/form/pit/<id>", methods=["POST"])
@login_required
def update_pit_form():
  form = request.form
  created_on = str(datetime.datetime.now())
  pits.add({
    # "photos": form.get("photos"),
    "scouter_name": form.get("scouter_name"),
    "team": form.get("team"),
    "base": form.get("base"),
    "dimensions": form.get("dimensions"),
    "weight": form.get("weight"),
    "algae_intake": form.get("algae_intake"),
    "coral_intake": form.get("coral_intake"),
    "L4": form.get("L4"),
    "L3": form.get("L3"),
    "L2": form.get("L2"),
    "L1": form.get("L1"),
    "auto_move": form.get("auto_move"),
    "auto_score": form.get("auto_score"),
    "auto_best_score": form.get("auto_best_score"),
    "shallow": form.get("shallow"),
    "deep": form.get("deep"),
    "comments": form.get("comments"),
    "updated_by": current_user.username,
    "updated_on": created_on,
    })

  return redirect("/scouting_dashboard")


@app.route("/scouting_dashboard", methods=["GET"])
def scouting_dashboard():

    return render_template("scouting_dashboard.html", bag=get_bag())

if CONFIG.PROD == False:

    socketio = SocketIO(app)

    @socketio.on('live reload')
    def handle_live_reload(message):
        log(message)


    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True, use_reloader=False)