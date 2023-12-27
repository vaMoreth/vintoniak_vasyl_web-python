from flask import jsonify, request
from app.todo.models import Todo
from app.auth.models import User
from datetime import datetime, timedelta
from app import db, basic_auth
from flask import jsonify, request, make_response
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required
from config import Config
from . import api_bp
from .. import db
import jwt

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return True
    return False


@api_bp.route('/login')
def login():
    auth = request.authorization

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('No such user in database', 401, {'WWW-Authenticate': 'Bearer realm="Authentication Required"'}) 

    if user.password == auth.password:
        expiry = datetime.utcnow() + timedelta(minutes=30)
        subject = "access"
        secret_key = Config.SECRET_KEY

        token = jwt.encode(
            {"sub": subject, "username": user.username, "exp": expiry},
            secret_key, 
            algorithm="HS256"
        )

        return jsonify({"token": token})

    return make_response('Invalid username or password', 401, {'WWW-Authenticate': 'Bearer realm="Authentication Required"'})


@api_bp.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    todos = Todo.query.all()
    todos_list = []
    for todo in todos:
        todos_list.append({
            'id': todo.id,
            'todo_item': todo.todo_item,
            'status': todo.status,
            'description': todo.description
        })
    return jsonify({'todos': todos_list})

@api_bp.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    data = request.json
    new_todo = Todo(
        todo_item=data.get('todo_item'),
        status=data.get('status', False),
        description=data.get('description')
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully'}), 201

@api_bp.route('/todos/<int:id>', methods=['GET'])
@jwt_required()
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return jsonify({
        'id': todo.id,
        'todo_item': todo.todo_item,
        'status': todo.status,
        'description': todo.description
    })

@api_bp.route('/todos/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.json
    todo.todo_item = data.get('todo_item', todo.todo_item)
    todo.status = data.get('status', todo.status)
    todo.description = data.get('description', todo.description)
    db.session.commit()
    return jsonify({'message': 'Todo updated successfully'}), 200

@api_bp.route('/todos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'}), 200
