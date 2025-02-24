from data import db

collection = "teams"

def getAll():
  return db.find(collection)