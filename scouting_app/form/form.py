import datetime
from flask import Blueprint, render_template, abort, request, redirect
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from scouting_app.data import forms
from scouting_app.data import teams


form_bp = Blueprint(
    'form', __name__,
    template_folder='templates'
)

@form_bp.route("/form/2024/new", methods=['GET'])
@login_required
def new_2024_form():
    vm = {
        "match_number": "",
        "starting_position": "Not There",
        "midline_collect": 1,
        "midline_time": 0,
        "intake": 1,
        "start_hang": 0,
        "stop_hang": 0,
        "end_status": 1,
        "comments": "",
        "options": get_form_options()
    }

    return render_template("2024_form.html", vm=vm, bag=get_bag())


@form_bp.route("/form/2024/new", methods=["POST"])
@login_required
def save_2024_form():
  form = request.form
  created_on = str(datetime.datetime.now())
  totalampshots = int(form.get("teleop_amp_score")) + int(form.get("teleop_amp_misses"))
  totalspeakershots = int(form.get("teleop_speaker_score")) + int(form.get("teleop_speaker_misses"))
  teleop_amp_accuracy = int(form.get("teleop_amp_score", 0)) / totalampshots
  teleop_speaker_accuracy = int(form.get("teleop_speaker_score", 0)) / totalspeakershots
  forms.add({
        "team": form.get("team"),
        "match_number": form.get("match_number"),
        "teleop_amp_accuracy": f"{teleop_amp_accuracy}",
        "teleop_speaker_accuracy": f"{teleop_speaker_accuracy}",
        "starting_position": form.get("starting_position"),
        "left_start": form.get("left_start"),
        "midline_collect": form.get("midline_collect"),
        "midline_time": form.get("midline_time"),
        "auto_amp_score": form.get("auto_amp_score"),
        "auto_amp_misses": form.get("auto_amp_misses"),
        "auto_speaker_score": form.get("auto_speaker_score"),
        "auto_speaker_misses": form.get("auto_speaker_misses"),
        "source_pickup": form.get("source_pickup"),
        "intake": form.get("intake"),
        "under_stage": form.get("under_stage"),
        "teleop_amp_score": form.get("teleop_amp_score"),
        "teleop_amp_misses": form.get("teleop_amp_misses"),
        "teleop_speaker_score": form.get("teleop_speaker_score"),
        "teleop_speaker_misses": form.get("teleop_speaker_misses"),
        "start_hang": form.get("start_hang"),
        "stop_hang": form.get("stop_hang"),
        "trap_score": form.get("trap_score"),
        "end_status": form.get("end_status"),
        "fell_over": form.get("fell_over"),
        "stopped_working": form.get("stopped_working"),
        "unstable_driving": form.get("unstable_driving"),
        "turned_off": form.get("turned_off"),
        "connection_issues": form.get("connection_issues"),
        "good_defense": form.get("good_defense"),
        "comments": form.get("comments"),
        "created_by": current_user.username,
        "updated_by": current_user.username,
        "created_on": created_on,
        "updated_on": created_on,
    })

  return redirect("/scouting_dashboard")


@form_bp.route("/form/2024/<id>", methods=['GET'])
@login_required
def load_2024_form(id):
    form = forms.get(id)

    vm = {
      "team": form.get("team"),
      "match_number": form.get("match_number"),
      "starting_position": form.get("starting_position"),
      "left_start": form.get("left_start"),
      "midline_collect": form.get("midline_collect"),
      "midline_time": form.get("midline_time"),
      "auto_amp_score": form.get("auto_amp_score"),
      "auto_amp_misses": form.get("auto_amp_misses"),
      "auto_speaker_score": form.get("auto_speaker_score"),
      "auto_speaker_misses": form.get("auto_speaker_misses"),
      "source_pickup": form.get("source_pickup"),
      "intake": form.get("intake"),
      "under_stage": form.get("under_stage"),
      "teleop_amp_score": form.get("teleop_amp_score"),
      "teleop_amp_misses": form.get("teleop_amp_misses"),
      "teleop_speaker_score": form.get("teleop_speaker_score"),
      "teleop_speaker_misses": form.get("teleop_speaker_misses"),
      "start_hang": form.get("start_hang"),
      "stop_hang": form.get("stop_hang"),
      "trap_score": form.get("trap_score"),
      "end_status": form.get("end_status"),
      "fell_over": form.get("fell_over"),
      "stopped_working": form.get("stopped_working"),
      "unstable_driving": form.get("unstable_driving"),
      "turned_off": form.get("turned_off"),
      "connection_issues": form.get("connection_issues"),
      "good_defense": form.get("good_defense"),
      "comments": form.get("comments"),
      "options": get_form_options()
    }

    return render_template("2024_form.html", vm=vm, bag=get_bag())


@form_bp.route("/form/2024/<id>", methods=["POST"])
@login_required
def update_2024_form(id):
  form = request.form
  totalampshots = int(form.get("teleop_amp_score")) + int(form.get("teleop_amp_misses"))
  totalspeakershots = int(form.get("teleop_speaker_score")) + int(form.get("teleop_speaker_misses"))
  teleop_amp_accuracy = int(form.get("teleop_amp_score", 0)) / totalampshots
  teleop_speaker_accuracy = int(form.get("teleop_speaker_score", 0)) / totalspeakershots

  forms.update(id, {
    "match_number": form.get("match_number"),
    "teleop_amp_accuracy": f"{teleop_amp_accuracy:.1%}",
    "teleop_speaker_accuracy": f"{teleop_speaker_accuracy:.1%}",
    "starting_position": form.get("starting_position"),
    "left_start": form.get("left_start"),
    "midline_collect": form.get("midline_collect"),
    "midline_time": form.get("midline_time"),
    "auto_amp_score": form.get("auto_amp_score"),
    "auto_amp_misses": form.get("auto_amp_misses"),
    "auto_speaker_score": form.get("auto_speaker_score"),
    "auto_speaker_misses": form.get("auto_speaker_misses"),
    "source_pickup": form.get("source_pickup"),
    "intake": form.get("intake"),
    "under_stage": form.get("under_stage"),
    "teleop_amp_score": form.get("teleop_amp_score"),
    "teleop_amp_misses": form.get("teleop_amp_misses"),
    "teleop_speaker_score": form.get("teleop_speaker_score"),
    "teleop_speaker_misses": form.get("teleop_speaker_misses"),
    "start_hang": form.get("start_hang"),
    "stop_hang": form.get("stop_hang"),
    "trap_score": form.get("trap_score"),
    "end_status": form.get("end_status"),
    "fell_over": form.get("fell_over"),
    "stopped_working": form.get("stopped_working"),
    "unstable_driving": form.get("unstable_driving"),
    "turned_off": form.get("turned_off"),
    "connection_issues": form.get("connection_issues"),
    "good_defense": form.get("good_defense"),
    "comments": form.get("comments"),
    "updated_by": current_user.username,
    "updated_on": str(datetime.datetime.now())
  })

  return redirect("/data")


def get_bag():
    return {
        "current_user": current_user.username
    }

def get_form_options():
    return {
        "teams": list(map(lambda team: team["name"], teams.getAll())),
        "starting_position": [
            "Not There",
            "Source",
            "Middle of Speaker",
            "Amp Side"
        ],
        "left_start": [
            "No",
            "Yes",
            "Attempted"
        ],
        "midline_collect": [
            "No",
            "Yes",
            "Attempted",
            "Ready for Teleop"
        ],
        "intake": [
            "Does not pick up from the floor",
            "Over the Bumper",
            "Under the Bumper"
        ],
        "end_status": [
            "Not Parked",
            "Parked",
            "Stage Attempted",
            "On Stage",
            "Hung with 1 Robot",
            "Hung with 2 Robots"
        ]
    }
