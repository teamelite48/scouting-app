print('🌱 Seeding MongoDB...');

app = db.getSiblingDB("scouting_app");

app.createCollection("2025_forms");
app.createCollection("qual_forms");
app.createCollection("pit_forms");
app.createCollection("users");
app.createCollection("teams");

forms = app.getCollection("2025_forms");

forms.insertOne({
  "scouter_name": "Elite Scouter",
  "age": "Test",
  "created_on": "2025-01-01 00:34:01.721103"
});

quals = app.getCollection("qual_forms");

quals.insertOne({
  "team": "Test",
  "match_number": "Test",
  "scouter_name": "Test",
  "comments": "Test",
  "created_by": "Test",
  "updated_by": "Test",
  "created_on": "2025-01-01 00:34:01.721103",
  "updated_on": "2025-01-01 00:34:01.721103",
});

pits = app.getCollection("pit_forms");

pits.insertOne({
  "scouter_name": "Test",
  "team": "Test",
  "base": "Test",
  "dimensions": "Test",
  "weight": "Test",
  "gravity": "Test",
  "algae_intake": "Test",
  "coral_intake": "Test",
  "L4": "Test",
  "L3": "Test",
  "L2": "Test",
  "L1": "Test",
  "auto_move": "Test",
  "auto_score": "Test",
  "auto_best_score": "Test",
  "shallow": "Test",
  "deep": "Test",
  "comments": "Test",
  "created_by": "Test",
  "updated_by": "Test",
  "created_on": "2025-01-01 00:34:01.721103",
  "updated_on": "2025-01-01 00:34:01.721103"
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
  "username": "D",
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

teams.insertOne({ "name": 48 });
teams.insertOne({ "name": 111 });
teams.insertOne({ "name": 112 });
teams.insertOne({ "name": 323 });
teams.insertOne({ "name": 1739 });
teams.insertOne({ "name": 1781 });
teams.insertOne({ "name": 2022 });
teams.insertOne({ "name": 2151 });
teams.insertOne({ "name": 2338 });
teams.insertOne({ "name": 2638 });
teams.insertOne({ "name": 3023 });
teams.insertOne({ "name": 3061 });
teams.insertOne({ "name": 3067 });
teams.insertOne({ "name": 3695 });
teams.insertOne({ "name": 4096 });
teams.insertOne({ "name": 4143 });
teams.insertOne({ "name": 4296 });
teams.insertOne({ "name": 4645 });
teams.insertOne({ "name": 4702 });
teams.insertOne({ "name": 4787 });
teams.insertOne({ "name": 4863 });
teams.insertOne({ "name": 5125 });
teams.insertOne({ "name": 5822 });
teams.insertOne({ "name": 7201 });
teams.insertOne({ "name": 7560 });
teams.insertOne({ "name": 8029 });
teams.insertOne({ "name": 8096 });
teams.insertOne({ "name": 8122 });
teams.insertOne({ "name": 8863 });
teams.insertOne({ "name": 8880 });
teams.insertOne({ "name": 9280 });
teams.insertOne({ "name": 9494 });
teams.insertOne({ "name": 9654 });
teams.insertOne({ "name": 9669 });
teams.insertOne({ "name": 9692 });
teams.insertOne({ "name": 10214 });
teams.insertOne({ "name": 10226 });
teams.insertOne({ "name": 10288 });
teams.insertOne({ "name": 10435 });
teams.insertOne({ "name": 10438 });
teams.insertOne({ "name": 10458 });


print('🏁 Finished seeding MongoDB');