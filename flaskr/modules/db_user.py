import sqlite3

DATABASE = "login.db"

def user_mail_lst(userID, mail):
    con = sqlite3.connect(DATABASE)
    existing_user = con.execute("SELECT userID FROM user WHERE userID = ?", (userID,)).fetchone()
    existing_mail = con.execute("SELECT mail FROM user WHERE mail = ?", (mail,)).fetchone()
    con.close()
    return existing_user, existing_mail

def user_passwd_lst(userID, passwd):
    con = sqlite3.connect(DATABASE)
    existing = con.execute("SELECT * FROM user WHERE userID = ? AND hashed_password = ?", (userID, passwd)).fetchall()
    con.close()
    return existing

def user_insert(userID, passWD, mail):
    con = sqlite3.connect(DATABASE)
    con.execute("INSERT INTO user VALUES(?, ?, ?)", (user['userID'], passWD, user['mail']))
    con.commit()
    con.close()
    return