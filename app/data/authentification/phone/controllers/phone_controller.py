from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from data.authentification.phone.schemas.login_validation_schema import LoginValidationSchema
from data.authentification.user.models.user_model import UserModel
from data.authentification.user.schemas.phone_user_schema import UserSchema
from shared.authentification.managers import PhoneAuthManager
from shared.authentification.managers.jwt_manager import JWTGenerationManager
from shared.utils.registry import Registry

NAME = "phone_auth"
blueprint = Blueprint(NAME + "_blueprint", __name__)

auth_manager = PhoneAuthManager()
jwt_manager = JWTGenerationManager()
login_validation_schema = LoginValidationSchema()
send_sms_validation_schema = UserSchema(only=["phone"])
user_schema = UserSchema()
user_registry = Registry(UserModel)


@blueprint.post(f"/{NAME}/register")
def register():
    data = request.get_json()
    user = user_schema.load(data)
    user_registry.save_entity(user)
    auth_manager.send_verification_message(user)
    return {"status": "SUCCES"}, 200


@blueprint.post(f"/{NAME}/send_sms")
def send_msg():
    data = request.get_json()
    send_sms_validation_schema.validate(data)
    user = user_registry.get_one_or_fail_where(phone=data["phone"])
    auth_manager.send_phone_msg(user)
    return {"status": "SUCCESS"}, 200


@blueprint.post(f"/{NAME}/login")
def login():
    data = request.get_json()
    login_validation_schema.validate(data)
    user = user_registry.get_one_or_fail_where(phone=data["phone"])
    auth_manager.authenticate_by_phone(user, data["code"])
    tokens = jwt_manager.generate_access_and_refresh_tokens(user.id)
    return tokens, 200


@jwt_required(refresh=True)
@blueprint.get(f"/{NAME}/refresh_token")
def refresh_token():
    user_id = get_jwt_identity()
    access_token = jwt_manager.generate_token(user_id)
    return {"access_token": access_token}, 200
