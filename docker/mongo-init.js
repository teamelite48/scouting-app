print('🌱 Seeding MongoDB...');

app = db.getSiblingDB("scouting_app");

app.createCollection("2024_matches");
app.createCollection("users");

matches = app.getCollection("2024_matches");

matches.insertOne({
  "scouter_name": "Elite Scouter",
  "age": 48
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

print('🏁 Finished seeding MongoDB');