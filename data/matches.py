from data import db


collection = "2024_matches"

def add(match):
  return db.insert_one(collection, match)

def getAll():
  return db.find(collection)

def get(id):
  return db.find_by_id(collection, id)

def update(id, match):
  return db.update_one(collection, id, match)