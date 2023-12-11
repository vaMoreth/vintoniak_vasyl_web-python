from .. import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_item = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(256))