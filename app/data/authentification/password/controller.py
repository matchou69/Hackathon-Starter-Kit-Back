from flask import Blueprint, request

from data.authentification.password.schema import LoginValidationSchema
from shared.authentification.managers import PasswordJwtManager

NAME = "password_auth"
blueprint = Blueprint(NAME + "_blueprint", __name__)

jwt_manager = PasswordJwtManager()
login_validation_schema = LoginValidationSchema()


@blueprint.post(f'/{NAME}/register')
def register():
    data = request.get_json()
    return jwt_manager.register_profile(data)


@blueprint.post(f'/{NAME}/login')
def login():
    data = request.get_json()
    login_validation_schema.validate(data)
    auth_token = jwt_manager.authenticate_user_by_name(data['username'], data['password'])
    if auth_token is None:                   
        return {'message': 'incorrect user or password'}
    return auth_token
