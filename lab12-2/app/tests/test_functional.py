import unittest
from flask import url_for, redirect
from flask_login import current_user
from .. import db
from app.auth.models import User
from app.todo.models import Todo
from .base import BaseTestCase


class SetupTest(BaseTestCase):

    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)
    

class PortfolioViewsTests(BaseTestCase):
    
    def test_home_page_loads(self):
        """
        GIVEN url to home page
        WHEN the '/home' page is requested (GET)
        THEN check that status code is 200 and response data contains '.Net Developer'
        """
        
        with self.client:
            response = self.client.get(url_for('portfolio.home'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'.Net Developer', response.data)
            
            
    def test_skills_page_loads(self):
        """
        GIVEN url to skills page
        WHEN the '/skills' page is requested (GET)
        THEN check that status code is 200 and response data contains 'Мої навички'
        """
        
        with self.client:
            response = self.client.get(url_for('portfolio.skills'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(u'Мої навички', response.data.decode('utf8'))
        

class AuthViewsTests(BaseTestCase):
    
    def test_login_page_loads(self):
        """
        GIVEN url to login page
        WHEN the '/login' page is requested (GET)
        THEN check that status code is 200 and response data contains 'Login'
        """
        
        with self.client:
            response = self.client.get(url_for('auth.login'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login', response.data)
    
    
    def test_register_page_loads(self):
        """
        GIVEN url to register page
        WHEN the '/register' page is requested (GET)
        THEN check that status code is 200 and response data contains 'Register'
        """
        
        with self.client:
            response = self.client.get(url_for('auth.register'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Register', response.data)


class AuthTests(BaseTestCase):
    
    def test_register_user_post(self):
        """
        GIVEN user data
        WHEN the register form is submitted (POST)
        THEN check that status code is 200, response data contains 'Register' 
            and registered user exist in DB with correct data (username)
        """
        
        with self.client:
            respons = self.client.post(
                url_for('auth.register'),
                data=dict(username='user2', email='user2@gmail.com', password='1234', confirm_password='1234'),
                follow_redirects=True
            )
            
            self.assertIn(b'Register', respons.data)
            user = User.query.filter_by(username='user2').first()
            assert respons.status_code == 200
            assert user is not None
            assert user.username == 'user2'
    

    def test_logout_user(self):
        """
        GIVEN user data
        WHEN the user is logged in and he logged out (POST)
        THEN check that status code is 200, response data contains 'You are logged out'
            and current_user is NOT authenticated3
        """
        
        with self.client:
            self.client.post(
                url_for('auth.login'),
                data=dict(username='user', password='1234'),
                follow_redirects = True
            )
            
            response = self.client.get(
                url_for('auth.logout'),
                follow_redirects = True
            )
            
            self.assertIn(b'You are logged out', response.data)
            assert response.status_code == 200
            assert current_user.is_authenticated == False


class TodoTests(BaseTestCase):
    
    def test_todo_create(self):
        """
        GIVEN todo data
        WHEN the todo created (POST)
        THEN check that status code is 200 and created todo exist in DB and stored corectly
        """
        
        data = {
            'todo_item': 'Write flask tests',  
            'description': 'New description', 
        }
        
        with self.client:
            response = self.client.post(
                url_for('todo.create_todo'),
                data=data, 
                follow_redirects=True
            )
            
            todo = Todo.query.filter_by(id=2).first()
            
            assert todo is not None
            assert todo.todo_item == data['todo_item']
            assert response.status_code == 200


    def test_get_all_todo(self):
        """
        GIVEN todos data
        WHEN the all existing todos queried (for ex. exist only 2 todos)
        THEN check that todo's count equal to 2
        """
        
        todo_1 = Todo(todo_item="todo1", description="description1")
        todo_2 = Todo(todo_item="todo2", description="description2")
        db.session.add_all([todo_1, todo_2])
        number_of_todos = Todo.query.count()
        assert number_of_todos == 3


    def test_update_todo_status(self):
        """
        GIVEN todo item
        WHEN the status field updated
        THEN response status code is 200 and todo.status is equal to True
        """
        todo_1 = Todo(todo_item="todo1", description="description1", status=False)
        db.session.add(todo_1)
        db.session.commit()

        todo_id = todo_1.id

        with self.client:
            response = self.client.post(
                f'/todo/edit/{todo_id}',
                data={
                    'todo_item': 'New Todo Item',
                    'description': 'New Description',
                    'status': True
                },
                follow_redirects=True
            )

            updated_todo = Todo.query.filter_by(id=todo_id).first()
            assert updated_todo.status is True
            assert response.status_code == 200



    def test_delete_todo(self):
        """
        GIVEN todo item
        WHEN the todo deleted
        THEN todo item does not exist and response status is 200
        """
        
        data = {
            'todo_item': 'Write flask tests',  
            'description': 'New description', 
        }
        
        with self.client:
            self.client.post(
                url_for('todo.todos'),
                data=data, 
                follow_redirects=True
            )
            
            response = self.client.get(
                url_for('todo.delete_todo', id=1),
                follow_redirects=True
            )
            
            todo = Todo.query.filter_by(id=1).first()
            assert response.status_code == 200
            assert todo is None
            
        

if __name__ == '__main__':
    unittest.main()