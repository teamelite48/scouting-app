from pymongo import MongoClient

from config import CONFIG


def find_one(collection, query):
  return _db_operation(collection, lambda db: db.find_one(query))

def insert_one(collection, document):
  return _db_operation(collection, lambda db: db.insert_one(document))

def update_one(collection, id, properties):
  return _db_operation(collection, lambda db: db.update_one({ "_id": id }, { "$set": properties }))


def _db_operation(collection, operation):

  client = MongoClient(CONFIG.MONGO_URI)
  db = client.get_database("scouting_app")

  result = operation(db.get_collection(collection))

  client.close()

  return result