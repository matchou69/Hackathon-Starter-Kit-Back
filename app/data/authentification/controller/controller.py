from flask import Blueprint, request

from shared.authentification.default_jwt_manager import register_profil, authenticate_user_by_name
from shared.authentification.schema.user_schema import UserSchema

NAME = 'auth'
blueprint = Blueprint(NAME + "_blueprint", __name__)

authentification_input = UserSchema(only=["username", "password"])


@blueprint.post('/register')
def register():
    data = request.get_json()
    return register_profil(data)

@blueprint.post('/login')
def login():
    data = request.get_json()
    data = authentification_input.load(data)
    auth_token = authenticate_user_by_name(data.username, data.password)
    if auth_token is None:
        return {'message': 'incorrect user or password'}
    return auth_token
