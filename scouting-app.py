from flask import Flask, render_template
from livereload import Server
from flask import request

app = Flask(__name__)
app.debug = True

forms = []

@app.route("/")
def base():
    return render_template("base.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/testing")
def testhub():
    return render_template("testing.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def registration():
    return render_template("registration.html")

@app.route("/manage")
def management():
    return render_template("manage.html")

@app.route("/dashboard/scoutingdash")
def scoutingdashboard():
    return render_template("scouting_dash.html")

@app.route("/dashboard/driveteam")
def drivedashboard():
    return render_template("drive_dash.html")

@app.route("/reports/upcoming")
def upcoming_match_reports():
    return render_template("upcoming.html")

@app.route("/reports/teamstats")
def team_stat_reports():
    return render_template("teamstats.html")

@app.route("/form/list")
def list_forms():
    return render_template("form_list.html", submissions=forms)

@app.route("/form", methods=['GET'])
def new_form():
    return render_template("match_form.html")



@app.route("/form", methods=["POST"])
def save_form():
    
    forms.append(request.form)

    print()
    print(str(forms))
    print()
    
    return new_form()



# server = Server(app.wsgi_app)
# server.watch("*.*")
# server.serve(port=5000)
