import bcrypt

from data.authentification.user.models.password_user_model import PasswordUserModel as UserModel
from data.authentification.user.schemas.password_user_schema import UserSchema
from shared.authentification.errors.password_error import WrongPasswordError
from shared.authentification.errors.username_not_found_error import UsernameNotFoundError
from shared.utils.registry import Registry

user_schema = UserSchema()


class PasswordAuthManager:
    """
    Authentication module using passwords.

    This module provides functions for registering user profiles, and authenticating users based on passwords.
    """

    user_registry = Registry(UserModel)

    def authenticate_user_by_name(self, username, password):
        """
        Authenticate a user by their username and password.

        :param username: The username for authentication.
        :param password: The user's password to be checked.

        :raises UserNotFoundException: If there is an issue with retrieving user information.
        """

        users = self.user_registry.get_all_where(username=username)
        print(users, flush=True)
        if len(users) == 0:
            raise UsernameNotFoundError(username)
        for user in users:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return user
        raise WrongPasswordError()
