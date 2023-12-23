from flask_testing import TestCase
from app import create_app
from app import db
from app.auth.models import User
from app.todo.models import Todo


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app = create_app('test')
        return app

    def setUp(self):
        db.create_all()
        user = User(username='user', email='user@gmail.com', password='1234')
        todo = Todo(todo_item='test todo', description='This is a description')
        db.session.add_all([user, todo])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()