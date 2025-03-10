from data import db


collection = "qual_forms"

def add(form):
  return db.insert_one(collection, form)

def getAll():
  return db.find(collection)

def get(id):
  return db.find_by_id(collection, id)

def update(id, form):
  return db.update_one(collection, id, form)
