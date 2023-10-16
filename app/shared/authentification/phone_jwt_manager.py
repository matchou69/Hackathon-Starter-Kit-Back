import random
from datetime import timedelta

from flask_jwt_extended import create_access_token
from marshmallow import fields, Schema

from shared import db, client
from shared.authentication.model.user_model import UserModel
from shared.authentication.schema.user_schema import UserSchema

class PhoneJwtManager:
    user_schema = UserSchema()
    code_pass = {}

    def generate_verification_code(self):
        """
        Generate a 6-digit random verification code.

        Returns:
            str: A randomly generated 6-digit verification code.
        """

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

    def register_profile(self, data):
        """
        Create a user in the database.

        Args:
            data: User data to be registered.

        Returns:
            str: "ok" if registration is successful.
        """

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

class LoginPhoneInput(Schema):
    phone = fields.String(required=True)
    code = fields.String(required=True)
