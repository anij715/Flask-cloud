import csv
import re
import sqlite3
import flask
from flask import (Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response)
DATABASE = "/var/www/html/flaskapp/users.db"
app = flask.Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'your secret key'

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def execute_query_one(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchone()
    cur.close()
    return rows

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=["GET","POST"])
def register():
        msg = ''
        
        if request.method == "POST" and 'username' in request.form and 'password' in request.form and 'email' in request.form :
            username = request.form['username']
            password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            
            x = cur.execute("""SELECT * FROM users WHERE username = ?""",
                          (username,)).fetchone()

            if x:
                msg = "That username is already taken, please choose another"
                return render_template('register.html', msg=msg)
            elif not re.match('[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
                return render_template('register.html', msg=msg)
            elif not re.match('[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers !'
                return render_template('register.html', msg=msg)
            elif not username or not password or not email:
                msg = 'Please fill out the form !'
                return render_template('register.html', msg=msg)
            else:
                cur.execute("""INSERT INTO users (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)""", (username, password, first_name, last_name, email))
                msg = "Thanks for registering!"

            conn.commit()
            conn.close()
         
            return redirect(url_for('viewdb'))
            #return redirect('http://127.0.0.1:5000/viewdb')
        elif request.method == 'POST':
            msg = 'Please fill out the form'
        return render_template("register.html", msg=msg)

@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM users""")
    return '<br>'.join(str(row) for row in rows)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password, ))
        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            msg = 'Logged in successfully !'
            return flask.redirect(url_for('viewdb'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
if __name__ == '__main__':
    app.run(debug=True)
