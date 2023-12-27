from flask import render_template
from flask_login import login_required
from . import users
from .. import navigation
from app.auth.models import User


@users.context_processor
def inject_navigation():
    return dict(navigation=navigation())

@users.route('/users')
@login_required
def user():
    all_users = User.query.all()
    total_users = len(all_users)
    return render_template('users.html', users=all_users, total_users=total_users)