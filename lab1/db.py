import json
from sqlite3 import connect

faculties={}

with open("lab1.json", "r", encoding="utf-8") as json_file:
    faculties = json.load(json_file)

connections = connect("lab2.db")
cursor = connections.cursor()

i = 0

for el in faculties:
    if el["departments"] != None:

        for el1 in el["departments"]:
            print(el1)
            try:
                cursor.execute(
                    "INSERT INTO departments (name, faculty) VALUES (?, ?)",
                    [el1, i]
                )

            except Exception:
                continue

    if el["staffs"] != None:
        for el1 in el["staffs"]:
            print(el1)
            try:
                cursor.execute(
                    "INSERT INTO staffs (name, faculty) VALUES (?, ?)",
                    [el1, i]
                )

            except Exception:
                continue
    cursor.execute(
        "INSERT INTO faculties (name, url) VALUES (?, ?)",
        [el['name'], el["url"]]
    )
    i+=1
    connections.commit()

connections.close()

print(faculties)