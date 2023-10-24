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
        return "Login failed. Please check your username and password."

@app.route('/info', methods=['GET', 'POST'])
def info():
    message = ""

    if 'username' in session:
        username = session['username']


        if request.method == 'POST':
            action = request.form.get('action')
            key = request.form.get('key')
            value = request.form.get('value')
            expiration = request.form.get('expiration')
            

            if action == 'add':
                if key and value and expiration:
                    expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=int(expiration))
                    response = make_response(render_template('info.html', username=username, message="Cookie added successfully"))
                    response.set_cookie(key, value, expires=expiration_time)
                    return response
                else:
                    message = "Invalid input for adding a cookie."
            elif action == 'delete':
                if key:
                    response = make_response(render_template('info.html', username=username, message="Cookie deleted successfully"))
                    response.delete_cookie(key)
                    return response
                else:
                    message = "Invalid input for deleting a cookie."
            else:
                message = "Invalid action."

        password_change_message = request.args.get('message')
        if password_change_message:
            message = password_change_message

        cookies = request.cookies
        cookie_data = []
        for key, value in cookies.items():
            if key.endswith('_expires'):
                continue

            expires_timestamp = request.cookies.get(key + '_expires')
            created_timestamp = request.cookies.get(key + '_created')

            if expires_timestamp is not None and created_timestamp is not None:
                expires = datetime.datetime.fromtimestamp(float(expires_timestamp))
                created = datetime.datetime.fromtimestamp(float(created_timestamp))
                cookie_data.append({'key': key, 'value': value, 'expiration': expires, 'created': created})

        return render_template('info.html', username=username, cookies=cookie_data, message=message)
    else:
        return redirect(url_for('home'))


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

            return redirect(url_for('info', message="Password changed successfully"))
        else:
            return redirect(url_for('info', message="Invalid new password"))

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
