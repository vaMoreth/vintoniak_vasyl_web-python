from datetime import datetime
from enum import Enum
from .. import db

class PostType(Enum):
    NEWS = 'news'
    PUBLICATION = 'publication'
    OTHER = 'other'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.String(1000))
    image = db.Column(db.String(255), default='postdefault.jpg')
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    type = db.Column(db.Enum(PostType), default=PostType.OTHER)
    enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Post('{self.title}', '{self.created}')"
