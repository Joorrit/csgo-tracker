"""Used to fix the database after a change in the code."""

import sqlite3


connection = sqlite3.connect("database.db")
cursor = connection.cursor()
#cursor.execute("DROP TABLE IF EXISTS positions")
