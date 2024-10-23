from data import db


collection = "2024_matches"

def save(match):
  return db.insert_one(collection, match)

def getAll():
  return db.find(collection)
