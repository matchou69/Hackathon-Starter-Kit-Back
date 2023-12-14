from flask import request, jsonify, Blueprint
from data.auth.schemas import UserSchema
from data.auth.models import UserModel
from marshmallow import ValidationError
from shared import db
import jwt
from datetime import datetime, timedelta

NAME= 'auth'

auth_blueprint = Blueprint(f"{NAME}_auth_blueprint", __name__)

from flask import jsonify

@auth_blueprint.post(f"{NAME}/register")
def register():
    data = request.json

    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']

    # Check if the username already exists in the database
    existing_user = UserModel.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already in use. Please choose a different username.'}), 400

    try:
        entity: UserModel = UserSchema().load(data)
    except ValidationError as error:
        return jsonify({'message': f"The payload doesn't correspond to a valid UserModel: {error}"}), 400

    db.session.add(entity)
    db.session.commit()

    return jsonify({'message': 'Registration successful', 'user': UserSchema().dump(entity)}), 200



@auth_blueprint.post(f"{NAME}/login")
def login():
    data = request.json

    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']

    user = UserModel.query.filter_by(username=username, password=password).first()

    if user:
        # Use a secret key securely stored in your application
        secret_key = 'your_secret_key'

        # Generate a JWT token
        token_payload = {'user_id': user.id_user, 'username': user.username}
        token = jwt.encode(token_payload, secret_key, algorithm='HS256')

        role = 'admin' if user.username == 'admin' else 'user'
        print(f"User found: {user.username}")
        print(f"Token generated: {token}")

        # Return the user ID, token, and role
        return jsonify({'message': 'Login successful', 'token': token, 'user_id': user.id_user, 'role': role}), 200
    else:
        # Debug print statement
        print("User not found")

        return jsonify({'message': 'Invalid credentials'}), 401


@auth_blueprint.get(f'{NAME}/get_user/<int:id>')
def get_user(id):
    user = UserModel.query.get(id)

    if not user:
        return jsonify({'message': 'User not found'}), 404
    user_data = {
        'id': user.id_user,
        'username': user.username,
        'password': user.password  # À noter que c'est généralement une mauvaise pratique
    }

    return jsonify({'user': user_data})


@auth_blueprint.get(f'{NAME}/get_all_users')
def get_all_users():
    users = UserModel.query.all()

    if not users:
        return jsonify({'message': 'No users found'}), 404

    user_data_list = []
    for user in users:
        user_data = {
            'id': user.id_user,
            'username': user.username,
            'password': user.password 
        }
        user_data_list.append(user_data)

    return jsonify({'users': user_data_list})


@auth_blueprint.delete(f'{NAME}/delete_user/<string:username>')
def delete_user(username):
    user = UserModel.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'})