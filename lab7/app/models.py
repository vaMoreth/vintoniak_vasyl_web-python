from . import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_item = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(256))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    message = db.Column(db.String(256), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='static/images/default.jpg')
    password = db.Column(db.String(60), nullable=False)