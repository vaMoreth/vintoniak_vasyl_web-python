from flask import Flask, render_template, request
import os
from datetime import datetime

app = Flask(__name__)

my_skills = [
    "Python",
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
    "Git",
    "C#",
]

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

@app.route('/resume')
def resume():
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('resume.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True)