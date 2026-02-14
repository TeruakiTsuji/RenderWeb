import sqlite3

DATABASE = 'login.db'

def create_expenses_table():
  con = sqlite3.connect(DATABASE)
  con.execute("CREATE TABLE IF NOT EXISTS user(userID VARCHAR PRIMARY KEY, hashed_password VARCHAR NOT NULL, mail VARCHAR NOT NULL)")
  con.close()
