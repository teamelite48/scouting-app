from data import db

collection = "scouters"

def getAll():
  return db.find(collection)