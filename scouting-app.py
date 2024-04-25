from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
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
