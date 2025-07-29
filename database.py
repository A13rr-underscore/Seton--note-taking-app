import sqlite3

conn = sqlite3.connect("Seton.db")
cursor = conn.cursor()

# Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        question1 TEXT,
        answer1 TEXT,
        question2 TEXT,
        answer2 TEXT
    )
''')
conn.commit()