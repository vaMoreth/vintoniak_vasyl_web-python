from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo, Email
from wtforms.validators import Regexp
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=20),
        Regexp('^[A-Za-z0-9_.]+$', message="Only letters, numbers, dots, or underscores are allowed.")
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please use a different email.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[InputRequired(), Length(min=4, max=10)])
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=4, max=10)])
    confirm_new_password = PasswordField('Confirm the new password', validators=[InputRequired(), Length(min=4, max=10)])
    submit = SubmitField('Change password')

class TodoForm(FlaskForm):
    todo_item = StringField('Todo Item', validators=[DataRequired()])
    status = BooleanField('Status')
    description = StringField('Description')
    submit = SubmitField('Submit')

class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')
