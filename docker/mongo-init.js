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

teams.insertOne({ "name": "34" })
teams.insertOne({ "name": "48" })
teams.insertOne({ "name": "144" })
teams.insertOne({ "name": "325" })
teams.insertOne({ "name": "432" })
teams.insertOne({ "name": "538" })
teams.insertOne({ "name": "744" })
teams.insertOne({ "name": "1038" })
teams.insertOne({ "name": "2190" })
teams.insertOne({ "name": "2220" })
teams.insertOne({ "name": "2338" })
teams.insertOne({ "name": "2502" })
teams.insertOne({ "name": "2783" })
teams.insertOne({ "name": "2973" })
teams.insertOne({ "name": "3058" })
teams.insertOne({ "name": "3138" })
teams.insertOne({ "name": "3140" })
teams.insertOne({ "name": "3468" })
teams.insertOne({ "name": "3630" })
teams.insertOne({ "name": "3814" })
teams.insertOne({ "name": "3824" })
teams.insertOne({ "name": "3843" })
teams.insertOne({ "name": "3959" })
teams.insertOne({ "name": "3966" })
teams.insertOne({ "name": "4020" })
teams.insertOne({ "name": "4028" })
teams.insertOne({ "name": "4265" })
teams.insertOne({ "name": "4601" })
teams.insertOne({ "name": "5005" })
teams.insertOne({ "name": "5045" })
teams.insertOne({ "name": "5125" })
teams.insertOne({ "name": "6107" })
teams.insertOne({ "name": "6302" })
teams.insertOne({ "name": "6517" })
teams.insertOne({ "name": "7072" })
teams.insertOne({ "name": "7111" })
teams.insertOne({ "name": "7428" })
teams.insertOne({ "name": "7725" })
teams.insertOne({ "name": "8624" })
teams.insertOne({ "name": "8772" })
teams.insertOne({ "name": "9097" })
teams.insertOne({ "name": "9410" })
teams.insertOne({ "name": "9590" })
teams.insertOne({ "name": "10011" })

print('🏁 Finished seeding MongoDB');