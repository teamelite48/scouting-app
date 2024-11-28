import bcrypt
import flask
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_socketio import SocketIO
from config import CONFIG
from data import matches
from data import users
from utils.log import log

login_manager = LoginManager()

app = Flask(__name__)
app.debug = CONFIG.DEBUG
app.secret_key = CONFIG.SECRET_KEY

login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(username):

    user = users.find(username)

    if (user.authenticated == False):
        return None

    return user


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    user = users.find(request.form.get("username"))

    formBytes = request.form.get("password").encode("UTF-8")
    userBytes = user.password.encode("UTF-8")

    if (bcrypt.checkpw(formBytes, userBytes)):
        user.authenticated = True
        users.save(user)
        login_user(user)
        next = flask.request.args.get("next")
        return flask.redirect(next or '/')

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
  return render_template("home.html", user_data={})


@app.route("/form/2024/new", methods=['GET'])
@login_required
def new_2024_form():

    vm = {
        "scouter_name": "",
        "starting_position": "1",
        "starting_position_options": [
            { "key": "1", "value": "Not There" },
            { "key": "2", "value": "Source" },
            { "key": "3", "value": "Middle of Speakers"},
            { "key": "4", "value": "Amp Side"}
        ],
        "starting_position": 1,
        "left_start_options": [
            { "key": "1", "value": "No" },
            { "key": "2", "value": "Yes" },
            { "key": "3", "value": "Attempted"}
        ],
        "midline_collect": 1,
        "midline_collect_options": [
            { "key": "1", "value": "No" },
            { "key": "2", "value": "Yes" },
            { "key": "3", "value": "Attempted"},
            { "key": "4", "value": "Ready for Teleop"}
        ],
        "midline_time": 0,
        "intake": 1,
        "intake_options": [
            { "key": "1", "value": "Does not pick up from the floor"},
            { "key": "2", "value": "Over the Bumper"},
            { "key": "3", "value": "Under the Bumper"}
        ],
        "starthang_time": 0,
        "stophang_time": 0,
        "end_status": 1,
        "end_status_options": [
            { "key": "1", "value": "Not Parked"},
            { "key": "2", "value": "Parked"},
            { "key": "3", "value": "Stage Attempted"},
            { "key": "4", "value": "On Stage" },
            { "key": "5", "value": "Hung with 1 Robot" },
            { "key": "6", "value": "Hung with 2 Robots"}
        ],
        "comments": ""
    }

    return render_template("2024_form.html", vm=vm)

@app.route("/form/2024/new", methods=["POST"])
@login_required
def save_2024_form():

  form = request.form

  matches.add({
    "scouter_name": form.get("scouter_name"),
    "starting_position": form.get("starting_position"),
    "left_starting_zone": form.get("left_starting_zone"),
    "midline_collected": form.get("midline_collected"),
    "midline_time": form.get("midline_time"),
    "auto_amp_score": form.get("auto_amp_score"),
    "auto_amp_misses": form.get("auto_amp_misses"),
    "auto_speaker_score": form.get("auto_speaker_score"),
    "auto_speaker_misses": form.get("auto_speaker_misses"),
    "source": form.get("source"),
    "intake": form.get("intake"),
    "under_stage": form.get("under_stage"),
    "teleop_amp_score": form.get("teleop_amp_score"),
    "teleop_amp_misses": form.get("teleop_amp_misses"),
    "teleop_speaker_score": form.get("teleop_speaker_score"),
    "teleop_speaker_misses": form.get("teleop_speaker_misses"),
    "start_hang": form.get("start_hang"),
    "stop_hang": form.get("stop_hang"),
    "trap_score": form.get("trap_score"),
    "end_of_match_state": form.get("end_of_match_state"),
    "fell_over": form.get("fell_over"),
    "stopped_working": form.get("stopped_working"),
    "unstable_driving": form.get("unstable_driving"),
    "turned_off": form.get("turned_off"),
    "connection_issues": form.get("connection_issues"),
    "good_defense": form.get("good_defense"),
    "comments": form.get("comments")
  })

  return redirect("/completed_matches")

@app.route("/form/2024/<id>", methods=['GET'])
@login_required
def load_2024_form(id):

    match = matches.get(id)

    vm = {
        "scouter_name": match.get("scouter_name"),
    }

    return render_template("2024_form.html", vm=vm)

@app.route("/form/2024/<id>", methods=["POST"])
@login_required
def update_2024_form(id):

  form = request.form

  matches.update(id, {
    "scouter_name": form.get("scouter_name"),
    "starting_position": form.get("starting_position"),
    "left_starting_zone": form.get("left_starting_zone"),
    "midline_collected": form.get("midline_collected"),
    "midline_time": form.get("midline_time"),
    "auto_amp_score": form.get("auto_amp_score"),
    "auto_amp_misses": form.get("auto_amp_misses"),
    "auto_speaker_score": form.get("auto_speaker_score"),
    "auto_speaker_misses": form.get("auto_speaker_misses"),
    "source": form.get("source"),
    "intake": form.get("intake"),
    "under_stage": form.get("under_stage"),
    "teleop_amp_score": form.get("teleop_amp_score"),
    "teleop_amp_misses": form.get("teleop_amp_misses"),
    "teleop_speaker_score": form.get("teleop_speaker_score"),
    "teleop_speaker_misses": form.get("teleop_speaker_misses"),
    "start_hang": form.get("start_hang"),
    "stop_hang": form.get("stop_hang"),
    "trap_score": form.get("trap_score"),
    "end_of_match_state": form.get("end_of_match_state"),
    "fell_over": form.get("fell_over"),
    "stopped_working": form.get("stopped_working"),
    "unstable_driving": form.get("unstable_driving"),
    "turned_off": form.get("turned_off"),
    "connection_issues": form.get("connection_issues"),
    "good_defense": form.get("good_defense"),
    "comments": form.get("comments")
  })

  return redirect("/completed_matches")


@app.route("/completed_matches", methods=['GET'])
@login_required
def completed_matches():
    return render_template("completed_matches.html", matches=matches.getAll())


if CONFIG.PROD == False:

    socketio = SocketIO(app)

    @socketio.on('live reload')
    def handle_live_reload(message):
        log(message)


    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True, use_reloader=False)