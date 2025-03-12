from data import db

collection = "teams"

def getAll():
  return db.find(collection)

def delete(id):
  return db.delete_one(collection, id)