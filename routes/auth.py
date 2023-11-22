from flask import Blueprint, render_template, redirect, url_for,flash,request,jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import User, Role, Task
from models.models import db
auth_bp = Blueprint('auth_bp', __name__)




@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')

    # Validate the role
    valid_roles = ['admin', 'manager', 'employee']
    if role not in valid_roles:
        return jsonify({'message': 'Invalid role. Choose a valid role: admin, manager, employee.'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists. Choose a different username.'}), 400

    new_user = User(username=username, password=password, email=email, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User signed up successfully!'})


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'message': 'Login unsuccessful. Please check your username and password.'}), 401

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


