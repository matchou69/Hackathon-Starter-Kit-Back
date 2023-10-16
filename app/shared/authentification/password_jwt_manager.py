from datetime import timedelta
import bcrypt
from flask_jwt_extended import create_access_token
from marshmallow import Schema, fields
from shared import db
from shared.authentication.model.user_model import UserModel
from shared.authentication.schema.user_schema import UserSchema

user_schema = UserSchema()

class PasswordJwtManager:
    """
    Authentication module for a project that uses passwords.

    This module provides functions for generating tokens, registering user profiles, and authenticating users based on passwords.
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
        Register a user's profile using the provided data.

        Args:
            data: User data to be registered.

        Returns:
            str: An access token for the registered user with a 2-hour expiration.

        Raises:
            Exception: If there is an issue with hashing the password or adding the user to the database.
        """

    def authenticate_user(self, id, password):
        """
        Authenticate a user by their ID and password.

        Args:
            id: The user's ID for authentication.
            password: The user's password to be checked.

        Returns:
            str: An access token for the authenticated user with a 2-hour expiration, or None if authentication fails.

        Raises:
            Exception: If there is an issue with retrieving user information or checking the password.
        """

    def authenticate_user_by_name(self, name, password):
        """
        Authenticate a user by their username and password.

        Args:
            name: The username for authentication.
            password: The user's password to be checked.

        Returns:
            str: An access token for the authenticated user with a 2-hour expiration, or None if authentication fails.

        Raises:
            Exception: If there is an issue with retrieving user information or checking the password.
        """

class AuthenticationInput(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
