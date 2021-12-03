import csv
import re
import sqlite3
DATABASE = "/var/www/html/flaskapp/users.db"
conn = sqlite3.connect(DATABASE)
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS users""")
cur.execute("""CREATE TABLE users
            (username text, password text, first_name text, last_name text, email text)""")

conn.commit()
conn.close()

