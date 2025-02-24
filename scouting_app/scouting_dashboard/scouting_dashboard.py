from flask import Blueprint, render_template, abort, redirect
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from operator import itemgetter
from scouting_app.data import forms


scouting_dashboard_bp = Blueprint(
    'scouting_dashboard', __name__,
    template_folder='templates'
)


@scouting_dashboard_bp.route("/")
@login_required
def home_page():
  return redirect("/scouting_dashboard")


@scouting_dashboard_bp.route("/scouting_dashboard", methods=["GET"])
def scouting_dashboard():
    return render_template("scouting_dashboard.html", bag=get_bag())


# @scouting_dashboard_bp.route('/', defaults={'page': 'index'})
# @scouting_dashboard_bp.route('/<page>')
# @login_required
# def show(page):
#     try:
#         return render_template(f'pages/{page}.html')
#     except TemplateNotFound:
#         abort(404)


@scouting_dashboard_bp.route("/data", methods=["GET"])
@login_required
def match_data():
    sorted_forms = sorted(forms.getAll(), key=itemgetter("created_on"), reverse=True)
    return render_template("match_data.html", forms=sorted_forms, bag=get_bag())


def get_bag():
    return {
        "current_user": current_user.username
    }
