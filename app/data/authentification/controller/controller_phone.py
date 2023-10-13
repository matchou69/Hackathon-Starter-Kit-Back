from flask import Blueprint, request
from marshmallow import Schema, fields

from shared.authentification.phone_jwt_manager import register_profil, send_phone_msg, authenticate_by_phone
from shared.authentification.schema.user_schema import UserSchema

NAME = 'auth'
blueprint = Blueprint(NAME + "_blueprint", __name__)

send_sms_input = UserSchema(only=["phone"])


class LoginPhoneInput(Schema):
    phone = fields.String()
    code = fields.String()

login_input = LoginPhoneInput()


@blueprint.post('/register')
def register():
    data = request.get_json()
    return register_profil(data)


@blueprint.post('/send_sms')
def send_msg():
    data = request.get_json()
    data = send_sms_input.load(data)
    if send_phone_msg(data.phone):
        return 'ok'
    return 'error'


@blueprint.post('/login')
def login():
    data = request.get_json()
    data = login_input.load(data)
    token = authenticate_by_phone(data['phone'], data['code'])
    if token is None:
        return 'error'
    return token
