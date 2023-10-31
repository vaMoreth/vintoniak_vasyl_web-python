from flask import Flask, make_response, render_template, request, redirect, url_for, session, flash
import json
import os
from datetime import datetime, timedelta
from forms import LoginForm

app = Flask(__name__)
app.secret_key = b"secret"
app.permanent_session_lifetime = timedelta(days=30)

my_skills = ["Python", "HTML", "CSS", "JavaScript", "SQL", "Git", "C#"]

with open('users.json', 'r') as f:
    users = json.load(f)

@app.route('/')
def home():
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('portfolio.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

@app.route('/portfolio')
def portfolio():
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('portfolio.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

@app.route('/skills')
@app.route('/skills/<int:id>')
def skills(id=None):
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if id is None:
        total_skills = len(my_skills)
        return render_template('skills.html', skills=my_skills, total_skills=total_skills, os_info=os_info, user_agent=user_agent, current_time=current_time)
    elif id < len(my_skills):
        return render_template('skill.html', skills=[my_skills[id]], id=id, os_info=os_info, user_agent=user_agent, current_time=current_time)
    else:
        return "Немає навички з таким id"
    
@app.route('/resume')
def resume():
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('resume.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in users and users[username] == password:
            session['username'] = username

            if form.remember.data:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)

            flash('Ви успішно увійшли', 'success')
            return redirect(url_for('info'))

        flash('Невірне ім\'я користувача або пароль', 'danger')

    flash('Необхідно увійти для доступу', 'warning')
    return render_template('login.html', form=form)

@app.route("/info", methods=['GET', 'POST'])
def info():
    if not session.get("username"):
        return redirect(url_for('login'))
    
    username = session.get("username")
    cookies = request.cookies
    return render_template("info.html", username=username, cookies=cookies)

@app.route('/setCookie', methods=["POST"])
def setCookie():
    key = request.form.get("key")
    value = request.form.get("value")
    days = request.form.get("days")
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
