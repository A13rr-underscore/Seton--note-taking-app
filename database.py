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

# Seton table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Seton (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT,
        category TEXT,
        mood TEXT,
        date TEXT,
        subject TEXT,
        topic TEXT,
        summary TEXT,
        folder INTEGER,
        username TEXT,
        FOREIGN KEY (username) REFERENCES Users (username)
    )
''')
conn.commit()