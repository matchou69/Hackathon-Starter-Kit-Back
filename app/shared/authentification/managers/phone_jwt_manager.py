import random

from twilio.base.exceptions import TwilioRestException

from data.authentification.user.model import UserModel
from shared import db, client
from shared.authentification.errors import UserNotFoundException, CustomTwilioError
from shared.authentification.utils import generate_token


class PhoneJwtManager:
    """
    Authentication module using phone numners.

    This module provides functions for registering user profiles, and authenticating users based on their phone number.
    """
    code_pass = {}

    def generate_verification_code(self):
        """
        Generate a 6-digit random verification code.

        :return: A randomly generated 6-digit verification code.
        """
        code = ''.join(str(random.randint(0, 9)) for _ in range(6))
        return code

    def register_profile(self, new_user: UserModel):
        """
        Create a user in the database.

        :param new_user: User entity to be registered.
        :return: "ok" if registration is successful.
        """

        db.session.add(new_user)
        db.session.commit()
        try:
            client.messages.create(
                from_='+13345183087',
                body='Bonjour ' + new_user.username + ' vous avez été enregistré à GeneeTech',
                to=new_user.phone)
        except TwilioRestException as twilio_error:
            raise CustomTwilioError(twilio_error)
        return 'ok'

    def send_phone_msg(self, phone: str):
        """
        Send an SMS with a verification code to the specified phone number.

        :param phone: The recipient's phone number.
        :return: True if the message is sent successfully, False if the user is not found.
        :raises TwilioException: If there is an issue with sending the SMS.
        """

        user = db.session.query(UserModel).filter_by(phone=phone).one_or_none()
        if user is None:
            raise UserNotFoundException(phone=phone)
        code = self.generate_verification_code()
        try:
            client.messages.create(
                from_='+13345183087',
                body='Bonjour ' + user.username + ' votre code est : ' + code,
                to=user.phone)
        except TwilioRestException as twilio_error:
            raise CustomTwilioError(twilio_error)
        self.code_pass[user.id] = code

    def authenticate_by_phone(self, phone: str, code: str):
        """
        Check if the provided phone number and code match and generate a token if they do.

        :param phone: The user's phone number.
        :param code: The verification code to check.
        :return: An access token if the provided code is correct, None otherwise.
        :raises UserNotFoundException: If there is an issue with retrieving user information.
        """

        user = db.session.query(UserModel).filter_by(phone=phone).one_or_none()
        if user is None:
            raise UserNotFoundException(phone=phone)
        if code == self.code_pass.get(user.id):
            self.code_pass.pop(user.id)
            return generate_token(user.username, user.id, 2)
        return None
