import sqlite3

db = sqlite3.connect('weather.db')

cur = db.cursor()
cur.execute('''
    create table city (
        id INTEGER PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        icon VARCHAR(50) NOT NULL,
        temp FLOAT NOT NULL,
        desc VARCHAR(50) NOT NULL,
        last_updated TIMESTAMP
    )
''')