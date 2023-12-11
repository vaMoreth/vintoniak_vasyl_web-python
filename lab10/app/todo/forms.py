from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class TodoForm(FlaskForm):
    todo_item = StringField('Todo Item', validators=[DataRequired()])
    status = BooleanField('Status')
    description = StringField('Description')
    submit = SubmitField('Submit')