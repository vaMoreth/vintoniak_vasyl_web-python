from app.auth.models import User
from app.post.models import Post
from app.todo.models import Todo
from app import db


def test_user_model():
    """
    GIVEN  a user model
    WHEN a new user is created 
    THEN check the email and password fields are defined correctly
    """
    
    user = User(username="user", email="user@gmail.com", password="1234")
    assert user.username == 'user'
    assert user.email == 'user@gmail.com'
    assert user.password == '1234'


def test_todo_model():
    """
    GIVEN  a todo model
    WHEN a new todo is created 
    THEN check the title and description fields are defined correctly
    """
    
    todo = Todo(todo_item = "todo title", description = "this is todo description")
    assert todo.todo_item == "todo title"
    assert todo.description == "this is todo description"


def test_post_model():
    """
    GIVEN a Post model
    WHEN a new Post is created
    THEN check the ...... are defined correctly
    """
    
    post = Post(title='Post_test', text='Text post test')
    assert post.title == 'Post_test'
    assert post.text == 'Text post test'