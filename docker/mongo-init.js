print('🌱 Seeding MongoDB...');

app = db.getSiblingDB("scouting_app");

app.createCollection("2024_forms");
app.createCollection("users");
app.createCollection("teams");

forms = app.getCollection("2024_forms");

forms.insertOne({
  "scouter_name": "Elite Scouter",
  "age": 48,
  "created_on": "2024-12-05 00:34:01.721103"
});

users = app.getCollection("users");

users.insertOne({
  "username": "A",
  "password": "$2b$12$Lao7omDmMROC8wewoi9LmOrKsEJI/2Z75D802ILccBbhJmwIT3oxu", // team0048
  "admin": false,
  "authenticated": false
});

users.insertOne({
  "username": "B",
  "password": "$2b$12$Lao7omDmMROC8wewoi9LmOrKsEJI/2Z75D802ILccBbhJmwIT3oxu", // team0048
  "admin": false,
  "authenticated": false
});


users.insertOne({
  "username": "C",
  "password": "$2b$12$Lao7omDmMROC8wewoi9LmOrKsEJI/2Z75D802ILccBbhJmwIT3oxu", // team0048
  "admin": false,
  "authenticated": false
});

users.insertOne({
  "username": "admin",
  "password": "$2b$12$GYboYCKQv1skkPKpwX7SzeP/deJLC5Unjsfb7tAnllQcmGK3NVjcS", // admin
  "admin": true,
  "authenticated": false
})

teams= app.getCollection("teams")

teams.insertOne({
  "name": "test team 1"
})

teams.insertOne({
  "name": "test team 2"
})


print('🏁 Finished seeding MongoDB');