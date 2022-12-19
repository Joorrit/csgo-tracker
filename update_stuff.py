"""Used to fix the database after a change in the code."""

import sqlite3


connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS position_size")
cursor.execute("DROP TABLE IF EXISTS prices")
cursor.execute("DROP TABLE IF EXISTS purchase_price")
cursor.execute("DROP TABLE IF EXISTS items")
