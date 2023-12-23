from wtforms import BooleanField, FileField, StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from .models import PostType

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    type = SelectField('Type', choices=[(choice.name, choice.value) for choice in PostType], validators=[DataRequired()])
    enabled = BooleanField('Enabled')
    image = FileField('Image')
    submit = SubmitField('Submit')
