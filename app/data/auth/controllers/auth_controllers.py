from flask import request, jsonify, Blueprint
from data.auth.schemas import UserSchema
from data.auth.models import UserModel
from marshmallow import ValidationError
from shared import db

NAME= 'auth'

auth_blueprint = Blueprint(f"{NAME}_auth_blueprint", __name__)

"""@auth_blueprint.post(f"{NAME}/register")
def register():
    data = request.json
    try:
        entity: UserModel = UserSchema().load(data)
    except ValidationError as error:
        return f"The payload does't correspond to a valid UserModel: {error}", 400

    db.session.add(entity)
    db.session.commit()

    return UserSchema().dump(entity), 200"""


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

    user = UserModel.query.filter_by(username=username).first()

    if user and user.password == password:
        # Here, you can generate a JWT token and return it in the response
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
