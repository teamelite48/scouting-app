from bson import ObjectId
from pymongo import MongoClient

from config import CONFIG


def find(collection, query={}):
  return _db_operation(collection, lambda db: db.find(query).to_list())

def find_one(collection, query):
  return _db_operation(collection, lambda db: db.find_one(query))

def find_by_id(collection, id):
  return _db_operation(collection, lambda db: db.find_one({ "_id": ObjectId(id) }))

def insert_one(collection, document):
  return _db_operation(collection, lambda db: db.insert_one(document))

def update_one(collection, id, properties):
  return _db_operation(collection, lambda db: db.update_one({ "_id": ObjectId(id) }, { "$set": properties }))

def delete_one(collection, id):
  return _db_operation(collection, lambda db: db.delete_one({ "_id": ObjectId(id) }))


def _db_operation(collection, operation):

  client = MongoClient(CONFIG.MONGO_URI)
  db = client.get_database("scouting_app")

  result = operation(db.get_collection(collection))

  client.close()

  return result