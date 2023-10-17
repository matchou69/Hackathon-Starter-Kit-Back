from flask import Blueprint, request

from data.authentification.password.schema import LoginValidationSchema
from shared.authentification.managers import PasswordJwtManager
from flask_jwt_extended import jwt_required, get_jwt_identity

NAME = "password_auth"
blueprint = Blueprint(NAME + "_blueprint", __name__)

jwt_manager = PasswordJwtManager()
login_validation_schema = LoginValidationSchema()


@blueprint.post(f'/{NAME}/register')
def register():
    data = request.get_json()
    tokens = jwt_manager.register_profile(data)
    return {'token': tokens[0],
            'refresh': tokens[1]}


@blueprint.post(f'/{NAME}/login')
def login():
    data = request.get_json()
    login_validation_schema.validate(data)
    tokens = jwt_manager.authenticate_user_by_name(data['username'], data['password'])
    if tokens is None:
        return {'message': 'incorrect user or password'}
    return {'token': tokens[0],
            'refresh': tokens[1]}


@jwt_required(refresh=True)
@blueprint.get(f'/{NAME}/refresh')
def refresh():
    current_id = get_jwt_identity()
    access_token = jwt_manager.refresh(current_id)
    return {'access_token': access_token}
