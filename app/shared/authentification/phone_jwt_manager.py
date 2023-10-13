from datetime import timedelta
import random

from flask_jwt_extended import create_access_token

from shared.authentification.model.user_model import UserModel
from shared import db

import bcrypt

from shared.authentification.schema.user_schema import UserSchema

from twilio.rest import Client

account_sid = 'ACbb113a454255d419c2b8de2c98b45427'
auth_token = 'bab92cb9c5f9f34b398acefc3c732f39'
client = Client(account_sid, auth_token)

from shared.utils import BaseCRUDHelper

user_schema = UserSchema()
code_pass = {}


def generate_verification_code():
    code = ''.join(str(random.randint(0, 9)) for _ in range(6))
    return code


def generate_token(user, additional_data, hour):
    expires = timedelta(hours=hour)
    additional_claims = {
        "custom_data": additional_data,
    }
    access_token = create_access_token(identity=user, expires_delta=expires, additional_claims=additional_claims)
    return access_token


def register_profil(data):
    new_user = user_schema.load(data)
    db.session.add(new_user)
    db.session.commit()
    client.messages.create(
        from_='+13345183087',
        body='Bonjour ' + new_user.username + ' vous avez été enregistré à GeneeTech' ,
        to=new_user.phone)
    return 'ok'

def send_phone_msg(phone):
    user = db.session.query(UserModel).filter_by(phone=phone).one_or_none()
    if user is None:
        return False
    code = generate_verification_code()
    client.messages.create(
        from_='+13345183087',
        body='Bonjour '+ user.username + ' votre code est : ' + code ,
        to=user.phone)
    code_pass[user.id] = code
    return True



def authenticate_by_phone(phone, code):
    user = db.session.query(UserModel).filter_by(phone=phone).one_or_none()
    if user is None:
        return None
    if code == code_pass[user.id]:
        return generate_token(user.username, user.id, 2)
    return None

