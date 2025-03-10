from flask import Flask, flash, redirect, render_template, request, url_for, session
from sqlite3 import *
from bcrypt import hashpw, gensalt, checkpw

app = Flask(__name__)

# __Database__

# Secret Key
app.secret_key = 'secret'

# Connect Database
def connect_db():
    conn = connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, password TEXT)')
    return conn

# Insert Data
def insert_db(name, password):
    conn = connect_db()
    conn.execute('INSERT INTO users (name, password) VALUES (?, ?)', (name, password))
    conn.commit()
    conn.close()

# Select Data
def select_db(name):
    conn = connect_db()
    cursor = conn.execute('SELECT * FROM users WHERE name = ?', (name,))
    data = cursor.fetchone()
    conn.close()
    return data

# __Routes__

# Index
@app.route('/')
def index():
    return render_template('index.html')

# Register
@app.route('/register' , methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        hash_pw = hashpw(password.encode('utf-8'), gensalt())
        insert_db(name, hash_pw)
        flash('Registered Successfully', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login
@app.route('/login' , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        user = select_db(name)
        if user and checkpw(password.encode('utf-8'), user[1]):
            session['username'] = name
            flash('Logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
        
    return render_template('login.html')

# Logout
@app.route('/logout', methods= ['GET', 'POST'])
def logout():
    session.pop('username', None)
    flash('Logged out', 'success')
    return redirect(url_for('index'))
    
# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)