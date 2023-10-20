import random

from data.authentification.user.models.user_model import UserModel
from shared import twilio_manager
from shared.authentification.errors import IncorrectVerificationCodeError


class PhoneAuthManager:
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
        code = "".join(str(random.randint(0, 9)) for _ in range(6))
        return code

    def send_verification_message(self, new_user: UserModel):
        """
        Sent verification message to the user

        :param new_user: User entity to be registered.
        :return: "ok" if registration is successful.
        """

        twilio_manager.send_message(
            to=new_user.phone,
            from_="+13345183087",
            body="Bonjour " + new_user.username + " vous avez été enregistré à GeneeTech",
        )

    def send_phone_msg(self, user: UserModel):
        """
        Send an SMS with a verification code to the specified phone number.

        :param user: The recipient.
        :return: True if the message is sent successfully, False if the user is not found.
        :raises TwilioException: If there is an issue with sending the SMS.
        """

        code = self.generate_verification_code()
        twilio_manager.send_message(
            to=user.phone,
            from_="+13345183087",
            body="Bonjour " + user.username + " votre code est : " + code,
        )
        self.code_pass[user.id] = code

    def authenticate_by_phone(self, user: UserModel, code: str):
        """
        Check if the provided phone number and code match and generate a token if they do.

        :param user: The user.
        :param code: The verification code to check.
        :return: An access token
        :raises UserNotFoundException: If there is an issue with retrieving user information.
        :raises IncorrectVerificationCodeError: If the provided code is not correct
        """
        if code == self.code_pass.get(user.id):
            self.code_pass.pop(user.id)
            return {"status": "SUCCESS"}
        raise IncorrectVerificationCodeError()
