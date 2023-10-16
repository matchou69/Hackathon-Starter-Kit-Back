import random
from datetime import timedelta

from flask_jwt_extended import create_access_token
from marshmallow import fields, Schema

from shared import db, client
from shared.authentification.model.user_model import UserModel
from shared.authentification.schema.user_schema import UserSchema


class PhoneJwtManager:
    user_schema = UserSchema()
    code_pass = {}

    def generate_verification_code(self):
        code = ''.join(str(random.randint(0, 9)) for _ in range(6))
        return code

    def generate_token(self, user, additional_data, hour):
        expires = timedelta(hours=hour)
        additional_claims = {
            "custom_data": additional_data,
        }
        access_token = create_access_token(identity=user, expires_delta=expires, additional_claims=additional_claims)
        return access_token

    def register_profil(self, data):
        new_user = self.user_schema.load(data)
        db.session.add(new_user)
        db.session.commit()
        client.messages.create(
            from_='+13345183087',
            body='Bonjour ' + new_user.username + ' vous avez été enregistré à GeneeTech',
            to=new_user.phone)
        return 'ok'

    def send_phone_msg(self, phone):
        user = db.session.query(UserModel).filter_by(phone=phone).one_or_none()
        if user is None:
            return False
        code = self.generate_verification_code()
        client.messages.create(
            from_='+13345183087',
            body='Bonjour ' + user.username + ' votre code est : ' + code,
            to=user.phone)
        self.code_pass[user.id] = code
        return True

    def authenticate_by_phone(self, phone, code):
        user = db.session.query(UserModel).filter_by(phone=phone).one_or_none()
        if user is None:
            return None
        if code == self.code_pass.get(user.id):
            self.code_pass.pop(user.id)
            return self.generate_token(user.username, user.id, 2)
        return None


class LoginPhoneInput(Schema):
    phone = fields.String(required=True)
    code = fields.String(required=True)
