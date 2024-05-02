from flask import Flask, render_template
from livereload import Server

app = Flask(__name__)
app.debug = True

import pickle
import os
from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True
user_data_file = "user_data.pickle"  # File to store user data

def load_user_data():
  """Loads user data from pickle file if it exists, otherwise returns an empty dictionary."""
  if os.path.exists(user_data_file):
    try:
      with open(user_data_file, "rb") as f:
        return pickle.load(f)
    except EOFError:
      # Handle potential empty file case (optional)
      return {}
  else:
    return {}
  
def save_user_data(data):
  """Saves user data to pickle file."""
  with open(user_data_file, "wb") as f:
    pickle.dump(data, f)
user_data = load_user_data()  # Load data on startup

@app.route("/home")
def home():
  return render_template("home.html", user_data=user_data)

@app.route("/testing", methods=["GET", "POST"])
def testhub():
  if request.method == "POST":
    # Get user input from the form
    new_data = request.form  # This is a dictionary containing form data
    user_data.update(new_data)  # Update user data with new input
    save_user_data(user_data)  # Save updated data
  return render_template("testing.html", user_data=user_data)


@app.route("/")
def base():
    return render_template("base.html")


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
