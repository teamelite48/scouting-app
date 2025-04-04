import bcrypt
from flask import Flask, render_template, request, redirect, jsonify
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_socketio import SocketIO
from config import CONFIG
from data import forms
from data import quals
from data import pits
from data import teams
from data import users
from utils.log import log
from datetime import datetime
import pprint
import sys
from operator import itemgetter


login_manager = LoginManager()

app = Flask(__name__)

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
        "team": sorted(list(map(lambda team: int(team["name"]), teams.getAll())) ),
        "match_number": ["Practice"] + [f"Qualification {i}" for i in range(1, 101)],
        "starting_position": [
            "Not There",
            "Barge side",
            "Middle",
            "Processor"
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
    return sorted(list(map(lambda team: int(team["name"]), teams.getAll())) )


@app.route("/data", methods=["GET"])
def match_data():

    vm = {
        "team": "",
        "options": get_teams()
    }

    sorted_forms = sorted(forms.getAll(), key=itemgetter("created_on"), reverse=True)

    sorted_quals = sorted(quals.getAll(), key=itemgetter("created_on"), reverse=True)

    sorted_pits = sorted(pits.getAll(), key=itemgetter("created_on"), reverse=True)

    return render_template("match_data.html", vm=vm, pits=sorted_pits, quals=sorted_quals, forms=sorted_forms, teams=get_teams(), bag=get_bag() )


@app.route("/team/lookup", methods=["GET"])
def team_lookup():

    return render_template("team_lookup.html", bag=get_bag(), teams=get_teams())

@app.route("/team/data", methods=["GET"])
def get_team_data():

    team = sorted(request.args.get("team") )

    sorted_forms = sorted(forms.find_by_team(team), key=itemgetter("created_on"), reverse=True)

    sorted_quals = sorted(quals.find_by_team(team), key=itemgetter("created_on"), reverse=True)

    sorted_pits = sorted(pits.find_by_team(team), key=itemgetter("created_on"), reverse=True)

    if team == "":
        return ""

    if not sorted_forms and not sorted_quals and not sorted_pits:
        return "No data found for team " + team

    vm = {
        "team": team,
        "teams": get_teams(),
        "summary": {
            "total_forms": len([form for form in sorted_forms if form.get('match_number') != "Practice"]),
            "average_coral_score": round(sum(form.get('total_coral_score', 0) for form in sorted_forms if form.get('match_number') != "Practice") / len([form for form in sorted_forms if form.get('match_number') != "Practice"]) if len([form for form in sorted_forms if form.get('match_number') != "Practice"]) != 0 else 0, 2),
            "average_algae_score": round(sum(form.get('total_algae_score', 0) for form in sorted_forms if form.get('match_number') != "Practice") / len([form for form in sorted_forms if form.get('match_number') != "Practice"]) if len([form for form in sorted_forms if form.get('match_number') != "Practice"]) != 0 else 0, 2),
            "average_processor_score": round(sum(form.get('total_processed', 0) for form in sorted_forms if form.get('match_number') != "Practice") / len([form for form in sorted_forms if form.get('match_number') != "Practice"]) if len([form for form in sorted_forms if form.get('match_number') != "Practice"]) != 0 else 0, 2),
            "average_coral_accuracy": f"{round(sum(float(form.get('teleop_coral_accuracy', '0').replace('%', '')) for form in sorted_forms if form.get('match_number') != 'Practice' and not (float(form.get('teleop_coral_accuracy', '0').replace('%', '')) == 0 and form.get('defended'))) / len([form for form in sorted_forms if form.get('match_number') != 'Practice' and not (float(form.get('teleop_coral_accuracy', '0').replace('%', '')) == 0 and form.get('defended'))]) if len([form for form in sorted_forms if form.get('match_number') != 'Practice' and not (float(form.get('teleop_coral_accuracy', '0').replace('%', '')) == 0 and form.get('defended'))]) != 0 else 0, 2):.2f}%",
            "average_algae_accuracy": f"{round(sum(float(form.get('teleop_algae_accuracy', '0').replace('%', '')) for form in sorted_forms if form.get('match_number') != 'Practice' and not (float(form.get('teleop_algae_accuracy', '0').replace('%', '')) == 0 and form.get('defended'))) / len([form for form in sorted_forms if form.get('match_number') != 'Practice' and not (float(form.get('teleop_algae_accuracy', '0').replace('%', '')) == 0 and form.get('defended'))]) if len([form for form in sorted_forms if form.get('match_number') != 'Practice' and not (float(form.get('teleop_algae_accuracy', '0').replace('%', '')) == 0 and form.get('defended'))]) != 0 else 0, 2):.2f}%",
            "average_processor_accuracy": f"{round(sum(float(form.get('teleop_processor_accuracy', '0').replace('%', '')) for form in sorted_forms if form.get('match_number') != 'Practice' and not (float(form.get('teleop_processor_accuracy', '0').replace('%', '')) == 0 and form.get('defended'))) / len([form for form in sorted_forms if form.get('match_number') != 'Practice' and not (float(form.get('teleop_processor_accuracy', '0').replace('%', '')) == 0 and form.get('defended'))]) if len([form for form in sorted_forms if form.get('match_number') != 'Practice' and not (float(form.get('teleop_processor_accuracy', '0').replace('%', '')) == 0 and form.get('defended'))]) != 0 else 0, 2):.2f}%",
            "total_L4": sum(int(form.get('total_L4', 0)) for form in sorted_forms if form.get('match_number') != "Practice"),
            "total_L3": sum(int(form.get('total_L3', 0)) for form in sorted_forms if form.get('match_number') != "Practice"),
            "total_L2": sum(int(form.get('total_L2', 0)) for form in sorted_forms if form.get('match_number') != "Practice"),
            "total_L1": sum(int(form.get('total_L1', 0)) for form in sorted_forms if form.get('match_number') != "Practice"),
            "total_algae_score": sum(int(form.get('total_algae_score', 0)) for form in sorted_forms if form.get('match_number') != "Practice"),
            "total_processed": sum(int(form.get('total_processed', 0)) for form in sorted_forms if form.get('match_number') != "Practice")
        }
    }

    return render_template("team_data.html", vm=vm, bag=get_bag(), pits=sorted_pits, quals=sorted_quals, forms=sorted_forms)



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
  total_L4 = int(form.get("teleop_L4_score") or 0) + int(form.get("auto_L4_score") or 0)
  total_L3 = int(form.get("teleop_L3_score") or 0) + int(form.get("auto_L3_score") or 0)
  total_L2 = int(form.get("teleop_L2_score") or 0) + int(form.get("auto_L2_score") or 0)
  total_L1 = int(form.get("teleop_L1_score") or 0) + int(form.get("auto_L1_score") or 0)
  
  created_on = str(datetime.now())
  forms.add({
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "scouter_name": form.get("scouter_name"),
    "teleop_coral_accuracy": f"{teleop_coral_accuracy:.2%}",
    "teleop_algae_accuracy": f"{teleop_algae_accuracy:.2%}",
    "teleop_processor_accuracy": f"{teleop_processor_accuracy:.2%}",
    "total_coral_score": total_coral_score,
    "total_algae_score": total_algae_score,
    "total_processed": total_processed,
    "total_L4": total_L4,
    "total_L3": total_L3,
    "total_L2": total_L2,
    "total_L1": total_L1,
    "no_auto": form.get("no_auto"),
    "defended": form.get("defended"),
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
        "no_auto": form.get("no_auto"),
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
        "defended": form.get("defended"),
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
  total_L4 = int(form.get("teleop_L4_score") or 0) + int(form.get("auto_L4_score") or 0)
  total_L3 = int(form.get("teleop_L3_score") or 0) + int(form.get("auto_L3_score") or 0)
  total_L2 = int(form.get("teleop_L2_score") or 0) + int(form.get("auto_L2_score") or 0)
  total_L1 = int(form.get("teleop_L1_score") or 0) + int(form.get("auto_L1_score") or 0)
  created_on = str(datetime.now())
  forms.update(id, {
    "team": form.get("team"),
    "match_number": form.get("match_number"),
    "scouter_name": form.get("scouter_name"),
    "teleop_coral_accuracy": f"{teleop_coral_accuracy:.2%}",
    "teleop_algae_accuracy": f"{teleop_algae_accuracy:.2%}",
    "teleop_processor_accuracy": f"{teleop_processor_accuracy:.2%}",
    "total_coral_score": total_coral_score,
    "total_algae_score": total_algae_score,
    "total_processed": total_processed,
    "total_L4": total_L4,
    "total_L3": total_L3,
    "total_L2": total_L2,
    "total_L1": total_L1,
    "no_auto": form.get("no_auto"),
    "defended": form.get("defended"),
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
        "match_number": ["Practice"] + [f"Qualification {i}" for i in range(1, 101)],
        "team": sorted(list(map(lambda team: int(team["name"]), teams.getAll())) )
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
  created_on = str(datetime.now())
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
  created_on = str(datetime.now())
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
        "team": sorted(list(map(lambda team: int(team["name"]), teams.getAll())) ),
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
  created_on = str(datetime.now())
  pits.add({
    # "photos": form.get("photos"),
    "team": form.get("team"),
    "scouter_name": form.get("scouter_name"),
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
        "team": form.get("team"),
        "scouter_name": form.get("scouter_name"),
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
        "options": get_pit_options()
    }

    return render_template("pit_form.html", vm=vm, bag=get_bag())

@app.route("/form/pit/<id>", methods=["POST"])
@login_required
def update_pit_form(id):
  form = request.form
  created_on = str(datetime.now())
  pits.update(id, 
    {
        # "photos": form.get("photos"),
        "team": form.get("team"),
        "scouter_name": form.get("scouter_name"),
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

@app.route("/htmx", methods=["GET"])
def htmx():
    return render_template("htmx.html", bag=get_bag())

@app.route("/team-data", methods=["POST"])
def team_data():
    return str(datetime.now())

@app.route("/petite_vue", methods=["GET"])
def petite():
    return render_template("petite_vue.html")

@app.route("/test_data", methods=["POST"])
def forms_data():
    return [
        { 'id': 1, 'name': 'Read' },
        { 'id': 2, 'name': 'Walk' },
        { 'id': 3, 'name': 'Yoga' }
    ]


if CONFIG.PROD == False:

    socketio = SocketIO(app)

    @socketio.on('live reload')
    def handle_live_reload(message):
        log(message)


    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True, use_reloader=False)