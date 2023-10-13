from datetime import timedelta

from flask_jwt_extended import create_access_token

from shared.authentification.model.user_model import UserModel
from shared import db

import bcrypt

from shared.authentification.schema.user_schema import UserSchema
from shared.utils import BaseCRUDHelper

user_schema = UserSchema()


def generate_token(user, additional_data, hour):
    expires = timedelta(hours=hour)
    additional_claims = {
        "custom_data": additional_data,
    }
    access_token = create_access_token(identity=user, expires_delta=expires, additional_claims=additional_claims)
    return access_token


def register_profil(data):
    new_user = user_schema.load(data)
    password = new_user.password
    hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user.password = hash_password
    db.session.add(new_user)
    db.session.commit()
    return generate_token(new_user.id, new_user.username, 2)


def authenticate_user(id, password):
    user = db.session.get(UserModel, id, with_for_update=True)
    if user is None:
        return None
    user = user_schema.dump(user)
    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return generate_token(user['username'], user['id'], 2)
    return None


def authenticate_user_by_name(name, password):
    users = db.session.query(UserModel).filter_by(username=name).all()
    for user in users:
        token = authenticate_user(user.id, password)
        if token is not None:
            return token
    return None

