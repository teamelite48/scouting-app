from flask import Blueprint, render_template, abort
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from jinja2 import TemplateNotFound


login_bp = Blueprint(
    'login', __name__,
    template_folder='templates'
)


@login_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


# @login_bp.route("/login", methods=["POST"])
# def login():
#     user = users.find(request.form.get("username"))

#     formBytes = request.form.get("password").encode("UTF-8")
#     userBytes = user.password.encode("UTF-8")

#     if (bcrypt.checkpw(formBytes, userBytes)):
#         user.authenticated = True
#         users.save(user)
#         login_user(user)
#         # next = flask.request.args.get("next")
#         # return flask.redirect(next or '/scouting-dashboard')
#         return redirect('/scouting_dashboard')

#     return render_template("/login.html")


# @login_bp.route("/logout", methods=["POST"])
# @login_required
# def logout():
#     user = users.find(current_user.username)
#     user.authenticated = False
#     users.save(user)

#     logout_user()

#     return redirect("/")


# @login_bp.user_loader
# def load_user(username):
#     user = users.find(username)

#     if (user.authenticated == False):
#         return None

#     return user
