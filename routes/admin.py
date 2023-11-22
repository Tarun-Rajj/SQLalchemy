from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity,User
from models.models import db, Task, User, Role

admin = Blueprint('admin', __name__)

@admin.route('/tasks', methods=['GET'])
@jwt_required()
def view_all_tasks():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if user.role.name == 'ADMIN':
        tasks = Task.query.all()
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.id,
                'title': task.title,
                'status': task.status,
                'assigned_to': task.assigned_to_user.username,
                'assigned_by': task.assigned_by_user.username
            })
        return jsonify(tasks=task_list), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 403

@admin.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def view_task(task_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    task = Task.query.get(task_id)

    if not task:
        return jsonify({'message': 'Task not found'}), 404

    if user.role.name == 'ADMIN':
        task_data = {
            'id': task.id,
            'title': task.title,
            'status': task.status,
            'assigned_to': task.assigned_to_user.username,
            'assigned_by': task.assigned_by_user.username
        }
        return jsonify(task_data), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 403

@admin.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if user.role.name == 'ADMIN':
        data = request.get_json()
        title = data.get('title')
        assigned_to_id = data.get('assigned_to')

        assigned_to_user = User.query.get(assigned_to_id)

        if assigned_to_user:
            task = Task(title=title, assigned_to=assigned_to_id, assigned_by=user.id)
            db.session.add(task)
            db.session.commit()

            return jsonify({'message': 'Task added successfully'}), 201
        else:
            return jsonify({'message': 'Invalid user ID'}), 400
    else:
        return jsonify({'message': 'Unauthorized'}), 403

@admin.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    task = Task.query.get(task_id)

    if not task:
        return jsonify({'message': 'Task not found'}), 404

    if user.role.name == 'ADMIN':
        data = request.get_json()
        new_status = data.get('status')

        if new_status in ['PENDING', 'IN PROGRESS', 'SENT FOR APPROVAL', 'APPROVED']:
            task.status = new_status
            db.session.commit()

            return jsonify({'message': 'Task status updated successfully'}), 200
        else:
            return jsonify({'message': 'Invalid task status'}), 400
    else:
        return jsonify({'message': 'Unauthorized'}), 403

@admin.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    task = Task.query.get(task_id)

    if not task:
        return jsonify({'message': 'Task not found'}), 404

    if user.role.name == 'ADMIN':
        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 403
