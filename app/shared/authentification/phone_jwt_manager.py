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
        """
        Generate a 6-digit random verification code.

        Returns:
            str: A randomly generated 6-digit verification code.
        """
        code = ''.join(str(random.randint(0, 9)) for _ in range(6))
        return code

    def generate_token(self, user, additional_data, hour):
        """
        Generate an access token with additional data.

        Args:
            user: The user for whom the token is generated.
            additional_data: Custom data to include in the token.
            hour: Token expiration time in hours.

        Returns:
            str: The generated access token.
        """
        expires = timedelta(hours=hour)
        additional_claims = {
            "custom_data": additional_data,
        }
        access_token = create_access_token(identity=user, expires_delta=expires, additional_claims=additional_claims)
        return access_token

    def register_profil(self, data):
        """
        Create a user in the database.

        Args:
            data: User data to be registered.

        Returns:
            str: "ok" if registration is successful.
        """
        new_user = self.user_schema.load(data)
        db.session.add(new_user)
        db.session.commit()
        client.messages.create(
            from_='+13345183087',
            body='Bonjour ' + new_user.username + ' vous avez été enregistré à GeneeTech',
            to=new_user.phone)
        return 'ok'

    def send_phone_msg(self, phone):
        """
        Send an SMS with a verification code to the specified phone number.

        Args:
            phone: The recipient's phone number.

        Returns:
            bool: True if the message is sent successfully, False if the user is not found.

        Raises:
            TwilioException: If there is an issue with sending the SMS.
        """
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
        """
        Check if the provided phone number and code match and generate a token if they do.

        Args:
            phone: The user's phone number.
            code: The verification code to check.

        Returns:
            str: An access token if the provided code is correct, None otherwise.

        Raises:
            KeyError: If the user is not found or if the code doesn't match.
        """

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
