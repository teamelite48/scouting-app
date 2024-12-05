print('🌱 Seeding MongoDB...');

app = db.getSiblingDB("scouting_app");

app.createCollection("2024_matches");
app.createCollection("users");
app.createCollection("scouters");

matches = app.getCollection("2024_matches");

matches.insertOne({
  "scouter_name": "Elite Scouter",
  "age": 48,
  "created_on": "2024-12-05 00:34:01.721103"
});

users = app.getCollection("users");

users.insertOne({
  "username": "elite",
  "password": "$2b$12$Lao7omDmMROC8wewoi9LmOrKsEJI/2Z75D802ILccBbhJmwIT3oxu", // team0048
  "full_name": "Elite Scouter",
  "admin": false,
  "authenticated": false
});

users.insertOne({
  "username": "admin",
  "password": "$2b$12$GYboYCKQv1skkPKpwX7SzeP/deJLC5Unjsfb7tAnllQcmGK3NVjcS", // admin
  "full_name": "Admin",
  "admin": true,
  "authenticated": false
})

scouters= app.getCollection("scouters")

scouters.insertOne({
  "name": "test scouter"
})
print('🏁 Finished seeding MongoDB');