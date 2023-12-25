from datetime import datetime
from flask import render_template, redirect, session, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from .forms import RegistrationForm, LoginForm, ChangePasswordForm, UpdateAccountForm
from collections import UserString
from .handler.account_handler import add_account_img
from . import auth
from .. import db, navigation
from .models import User
import secrets
import os

@auth.context_processor
def inject_navigation():
    return dict(navigation=navigation())

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('portfolio.home'))

        flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user() 
    flash('You are logged out', 'success')
    return redirect(url_for('portfolio.home'))

@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if 'username' in session:
            new_password = form.new_password.data

            if new_password:
                username = session['username']
                UserString[username] = new_password

                flash("Пароль успішно змінено", "success")
                return redirect(url_for('auth.login'))

    return render_template('change_password.html', form=form)

@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        
        if form.picture.data:
            print("We in IFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF!")
            image = add_account_img(form.picture.data)
            current_user.image_file = image

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('auth.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    return render_template('account.html', form=form)


@auth.after_request
def after_request(response):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while updating user last seen!', 'danger')
    return response