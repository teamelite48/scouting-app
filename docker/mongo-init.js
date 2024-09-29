print('🌱 Seeding MongoDB...');

scoutingApp = db.getSiblingDB("scouting_app");
scoutingApp.createCollection("2024_matches");

matches = scoutingApp.getCollection("2024_matches");

matches.insertOne({
  "scouter_name": "Elite Scouter",
  "age": 48
});

print('🏁 Finished seeding MongoDB');