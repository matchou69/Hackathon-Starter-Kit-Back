import bcrypt

from data.authentification.user.model import UserModel
from data.authentification.user.schema import UserSchema
from shared import db
from shared.authentification.errors import UserNotFoundException
from shared.authentification.utils import generate_token

user_schema = UserSchema()


class PasswordJwtManager:
    """
    Authentication module using passwords.

    This module provides functions for registering user profiles, and authenticating users based on passwords.
    """

    def register_profile(self, data):
        """
        Register a user's profile using the provided data.

        :param data: User data to be registered.
        :return: An access token for the registered user with a 2-hour expiration.
        :raise Exception: If there is an issue with hashing the password or adding the user to the database.
        """
        new_user = user_schema.load(data)
        password = new_user.password
        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user.password = hash_password
        db.session.add(new_user)
        db.session.commit()
        return generate_token(new_user.id, new_user.username, 2)

    def authenticate_user_by_id(self, id, password):
        """
        Authenticate a user by their ID and password.

        :param id: The user's database ID for authentication.
        :param password: The user's password to be checked.
        :return: An access token for the authenticated user with a 2-hour expiration, or None if authentication fails.

        :raises UserNotFoundException: If there is an issue with retrieving user information.
        :raises CustomTwilioError: If there is an issue checking the password.
        """

        user = db.session.get(UserModel, id, with_for_update=True)
        if user is None:
            raise UserNotFoundException(id=id)
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return generate_token(user.id, None, 2)
        return None

    def authenticate_user_by_name(self, name, password):
        """
        Authenticate a user by their username and password.

        :param name: The username for authentication.
        :param password: The user's password to be checked.
        :return: An access token for the authenticated user with a 2-hour expiration, or None if authentication fails.

        :raises UserNotFoundException: If there is an issue with retrieving user information.
        """

        users = db.session.query(UserModel).filter_by(username=name).all()
        if len(users) == 0:
            raise UserNotFoundException(name=name)
        for user in users:
            token = self.authenticate_user_by_id(user.id, password)
            if token is not None:
                return token
        return None
