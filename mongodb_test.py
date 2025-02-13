from pymongo import MongoClient

uri = "mongodb://mongo:mongo@localhost:27017/"
client = MongoClient(uri)

try:
  db = client.get_database("scouting_app")
  forms = db.get_collection("2025_forms")

  form = forms.find().to_list()

  print(form)

  client.close()

except Exception as e:
  raise Exception("Unable to find the document due to the following error: ", e)