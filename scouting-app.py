from flask import Flask, render_template
from livereload import Server

app = Flask(__name__)
app.debug = True

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

@app.route("/scoutingdash")
def scoutingdashboard():
    return render_template("scouting_dash.html")

@app.route("/drivedash")
def drivedashboard():
    return render_template("drive_dash.html")


server = Server(app.wsgi_app)
server.watch("templates/*.*")
server.serve(port=5000)
