from data import db
# from flask_login import UserMixin


collection = "users"

class User():

  def __init__(self, user):
    self.id = user["_id"]
    self.username = user["username"]
    self.password = user["password"]
    self.admin = user["admin"]
    self.authenticated = user["authenticated"]

  def is_active(self):
    return True

  def get_id(self):
    return self.username

  def is_authenticated(self):
    return self.authenticated

  def is_anonymous(self):
    return False


def find(username):
    user = db.find_one(collection, { "username": username })
    return User(user)

def save(user):
  db.update_one(collection, user.id, { "authenticated": user.authenticated })
