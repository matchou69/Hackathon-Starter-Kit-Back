from flask import Blueprint, request

from shared.authentification.password_jwt_manager import PasswordJwtManager, AuthentificationInput

NAME = 'auth'
blueprint = Blueprint(NAME + "_blueprint", __name__)

jwt_manager = PasswordJwtManager()


@blueprint.post('/register')
def register():
    data = request.get_json()
    return jwt_manager.register_profil(data)


@blueprint.post('/login')
def login():
    data = request.get_json()
    data = AuthentificationInput().validate(data)
    auth_token = jwt_manager.authenticate_user_by_name(data['username'], data['password'])
    if auth_token is None:
        return {'message': 'incorrect user or password'}
    return auth_token
