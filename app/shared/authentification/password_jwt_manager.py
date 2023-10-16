from datetime import timedelta

import bcrypt
from flask_jwt_extended import create_access_token
from marshmallow import Schema, fields

from shared import db
from shared.authentification.model.user_model import UserModel
from shared.authentification.schema.user_schema import UserSchema

user_schema = UserSchema()


class PasswordJwtManager:
    def generate_token(self, user, additional_data, hour):
        expires = timedelta(hours=hour)
        additional_claims = {
            "custom_data": additional_data,
        }
        access_token = create_access_token(identity=user, expires_delta=expires, additional_claims=additional_claims)
        return access_token

    def register_profil(self, data):
        new_user = user_schema.load(data)
        password = new_user.password
        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user.password = hash_password
        db.session.add(new_user)
        db.session.commit()
        return self.generate_token(new_user.id, new_user.username, 2)

    def authenticate_user(self, id, password):
        user = db.session.get(UserModel, id, with_for_update=True)
        if user is None:
            return None
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return self.generate_token(user.username, user['id'], 2)
        return None

    def authenticate_user_by_name(self, name, password):
        users = db.session.query(UserModel).filter_by(username=name).all()
        for user in users:
            token = self.authenticate_user(user.id, password)
            if token is not None:
                return token
        return None


class AuthentificationInput(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
