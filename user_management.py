import sqlite3 as sql
import time
import random
import html


def insertUser(username, password, DoB):
    with sql.connect("database_files/database.db") as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO users (username, password, dateOfBirth) VALUES (?, ?, ?)",
            (username, password, DoB),
        )


def retrieveUsers(username, password):
    with sql.connect("database_files/database.db") as con:
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = cur.fetchone()

    if not user:
        return False

    # Update visitor log safely
    try:
        with open("visitor_log.txt", "r+") as file:
            number = int(file.read().strip())
            file.seek(0)
            file.write(str(number + 1))
            file.truncate()
    except FileNotFoundError:
        with open("visitor_log.txt", "w") as file:
            file.write("1")

    time.sleep(random.randint(80, 90) / 1000)
    return True


def insertFeedback(feedback):
    with sql.connect("database_files/database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO feedback (feedback) VALUES (?)", (feedback,))


def listFeedback():
    with sql.connect("database_files/database.db") as con:
        cur = con.cursor()
        data = cur.execute("SELECT * FROM feedback").fetchall()

    with open("templates/partials/success_feedback.html", "w") as f:
        for row in data:
            safe_text = html.escape(row[1])
            f.write(f"<p>\n{safe_text}\n</p>\n")
