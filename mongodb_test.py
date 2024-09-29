from pymongo import MongoClient

uri = "mongodb://mongo:mongo@localhost:27017/"
client = MongoClient(uri)

try:
  db = client.get_database("scouting_app")
  matches = db.get_collection("2024_matches")

  match = matches.find_one()

  print(match)

  client.close()

except Exception as e:
  raise Exception("Unable to find the document due to the following error: ", e)