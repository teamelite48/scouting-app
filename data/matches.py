from data import db


collection = "2024_matches"

def add(match):
  return db.insert_one(collection, match)
