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

teams.insertOne({
  "name": "test team 1"
})

teams.insertOne({
  "name": "test team 2"
})

teams.insertOne({
  "name": "test team 3"
})

teams.insertOne({
  "name": "test team 4"
})

teams.insertOne({
  "name": "test team 5"
})

teams.insertOne({
  "name": "test team 6"
})

print('🏁 Finished seeding MongoDB');