from flask import Flask, make_response, render_template, request, redirect, url_for, session
import json
import datetime

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
        return "Помилка логіну. Перевірте своє ім'я користувача та пароль."
    
@app.route("/info", methods=['GET', 'POST'])
def info():
    
    if not session.get("username"):
        ("Please check the box 'remember me'", "danger")
        return redirect(url_for('login'))
    
    username = session.get("username")
    cookies = request.cookies
    return render_template("info.html", username=username, cookies=cookies)

@app.route('/setCookie', methods=["POST"])
def setCookie():
    key = request.form.get("key")
    value = request.form.get("value")
    days = request.form.get("days")
    #message = "Cookie successfully set"
    response = make_response(redirect(url_for('info')))
    response.set_cookie(key, value, max_age=60*60*24*int(days))
    return response

@app.route("/deleteCookieByKey", methods=["POST"])
def deleteCookieByKey():
    key = request.form.get("key")
    response = make_response(redirect(url_for('info')))
    response.delete_cookie(key) 
    return response


@app.route("/deleteCookieAll", methods=["POST"])
def deleteCookieAll():
    cookiesKeys = request.cookies
    response = make_response(redirect(url_for('info')))
    
    for key, value in cookiesKeys.items():
        if key != "session":
            response.delete_cookie(key)
    return response

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'username' in session:
        new_password = request.form.get('new_password')

        if new_password:
            username = session['username']
            users[username] = new_password

            return redirect(url_for('home', message="Пароль успішно змінено"))
        else:
            return redirect(url_for('info', message="Недійсний новий пароль"))

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
