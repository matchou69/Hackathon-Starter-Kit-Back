from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from data.authentification.password.schemas.login_validation_schema import LoginValidationSchema
from data.authentification.user.models.user_model import UserModel
from data.authentification.user.schemas.password_user_schema import UserSchema
from shared.authentification.managers import PasswordAuthManager
from shared.authentification.managers.jwt_manager import JWTGenerationManager
from shared.utils.registry import Registry

NAME = "password_auth"
blueprint = Blueprint(NAME + "_blueprint", __name__)

auth_manager = PasswordAuthManager()
jwt_manager = JWTGenerationManager()
login_validation_schema = LoginValidationSchema()
user_schema = UserSchema()
user_registry = Registry(UserModel)


@blueprint.post(f"/{NAME}/register")
def register():
    data = request.get_json()
    user = user_schema.load(data)
    user_registry.save_entity(user)
    return jwt_manager.generate_access_and_refresh_tokens(user.id), 200


@blueprint.post(f"/{NAME}/login")
def login():
    data = request.get_json()
    login_validation_schema.load(data)
    user = auth_manager.authenticate_user_by_name(data["username"], data["password"])
    return jwt_manager.generate_access_and_refresh_tokens(user.id), 200


@jwt_required(refresh=True)
@blueprint.get(f"/{NAME}/refresh_token")
def refresh_token():
    user_id = get_jwt_identity()
    access_token = jwt_manager.generate_token(user_id, is_refresh=True)
    return {"access_token": access_token}, 200
