from pymongo import MongoClient


uri = "mongodb://mongo:mongo@db:27017/"

def insert_one(collection, document):
  return _db_operation(collection, lambda db: db.insert_one(document))


def _db_operation(collection, operation):

  client = MongoClient(uri)
  db = client.get_database("scouting_app")

  result = operation(db.get_collection(collection))

  client.close()

  return result