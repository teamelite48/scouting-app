print('🌱 Seeding MongoDB...');

app = db.getSiblingDB("scouting_app");

app.createCollection("2025_forms");
app.createCollection("qual_forms");
app.createCollection("pit_forms");
app.createCollection("users");
app.createCollection("teams");

forms = app.getCollection("2025_forms");

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

teams.insertOne({ "name": "48" });
teams.insertOne({ "name": "120" });
teams.insertOne({ "name": "128" });
teams.insertOne({ "name": "291" });
teams.insertOne({ "name": "677" });
teams.insertOne({ "name": "695" });
teams.insertOne({ "name": "1308" });
teams.insertOne({ "name": "1405" });
teams.insertOne({ "name": "1511" });
teams.insertOne({ "name": "1559" });
teams.insertOne({ "name": "1787" });
teams.insertOne({ "name": "2172" });
teams.insertOne({ "name": "2228" });
teams.insertOne({ "name": "2252" });
teams.insertOne({ "name": "2399" });
teams.insertOne({ "name": "2603" });
teams.insertOne({ "name": "3015" });
teams.insertOne({ "name": "3173" });
teams.insertOne({ "name": "3193" });
teams.insertOne({ "name": "3260" });
teams.insertOne({ "name": "3484" });
teams.insertOne({ "name": "3777" });
teams.insertOne({ "name": "3954" });
teams.insertOne({ "name": "4050" });
teams.insertOne({ "name": "4085" });
teams.insertOne({ "name": "4121" });
teams.insertOne({ "name": "4145" });
teams.insertOne({ "name": "4269" });
teams.insertOne({ "name": "4601" });
teams.insertOne({ "name": "4611" });
teams.insertOne({ "name": "4991" });
teams.insertOne({ "name": "5413" });
teams.insertOne({ "name": "5740" });
teams.insertOne({ "name": "6181" });
teams.insertOne({ "name": "6964" });
teams.insertOne({ "name": "7165" });
teams.insertOne({ "name": "7717" });
teams.insertOne({ "name": "7885" });
teams.insertOne({ "name": "8140" });
teams.insertOne({ "name": "8145" });
teams.insertOne({ "name": "8222" });
teams.insertOne({ "name": "8243" });
teams.insertOne({ "name": "8393" });
teams.insertOne({ "name": "8713" });
teams.insertOne({ "name": "8718" });
teams.insertOne({ "name": "9139" });
teams.insertOne({ "name": "9194" });
teams.insertOne({ "name": "9545" });
teams.insertOne({ "name": "9622" });
teams.insertOne({ "name": "9643" });
teams.insertOne({ "name": "9653" });
teams.insertOne({ "name": "9767" });
teams.insertOne({ "name": "10207" });
teams.insertOne({ "name": "10208" });
teams.insertOne({ "name": "10303" });
teams.insertOne({ "name": "10582" });


print('🏁 Finished seeding MongoDB');