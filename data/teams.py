from data import db

collection = "teams"

def getAll():
  return db.find(collection)

def get_all_sorted():
    return sorted(list(map(lambda team: int(team["name"]), getAll())) )