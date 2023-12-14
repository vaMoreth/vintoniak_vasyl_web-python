from flask import Blueprint, jsonify, request
from app.todo.models import Todo
from .. import db

api_todo = Blueprint('api_todo', __name__, url_prefix='/api/todos')

@api_todo.route('/', methods=['GET'])
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

@api_todo.route('/', methods=['POST'])
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

@api_todo.route('/<int:id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return jsonify({
        'id': todo.id,
        'todo_item': todo.todo_item,
        'status': todo.status,
        'description': todo.description
    })

@api_todo.route('/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.json
    todo.todo_item = data.get('todo_item', todo.todo_item)
    todo.status = data.get('status', todo.status)
    todo.description = data.get('description', todo.description)
    db.session.commit()
    return jsonify({'message': 'Todo updated successfully'}), 200

@api_todo.route('/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'}), 200
