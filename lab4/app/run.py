from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = b"secret"

with open('users.json', 'r') as f:
    users = json.load(f)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('info'))
    else:
        return "Login failed. Please check your username and password."

@app.route('/info')
def info():
    if 'username' in session:
        username = session['username']
        return render_template('info.html', username=username)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
