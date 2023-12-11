from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm


class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')