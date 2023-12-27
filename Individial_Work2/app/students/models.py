from app import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    course = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Student {self.name} {self.surname}"
