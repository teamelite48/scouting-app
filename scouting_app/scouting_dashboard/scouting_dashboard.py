from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from operator import itemgetter
import importlib
data_module = importlib.import_module("data")
forms = data_module.forms


scouting_dashboard_bp = Blueprint(
    'scouting_dashboard', __name__,
    template_folder='templates'
)

@scouting_dashboard_bp.route('/', defaults={'page': 'index'})
@scouting_dashboard_bp.route('/<page>')
@login_required
def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)


@scouting_dashboard_bp.route("/scouting_dashboard", methods=['GET'])
@login_required
def scouting_dashboard():
    sorted_forms = sorted(forms.getAll(), key=itemgetter("created_on"), reverse=True)
    return render_template("scouting_dashboard.html", forms=sorted_forms, bag=get_bag())


def get_bag():
    return {
        "current_user": current_user.username
    }
