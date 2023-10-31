from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[InputRequired(), Length(min=4, max=10)])
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=4, max=10)])
    confirm_new_password = PasswordField('Confirm the new password', validators=[InputRequired(), Length(min=4, max=10)])
    submit = SubmitField('Change password')