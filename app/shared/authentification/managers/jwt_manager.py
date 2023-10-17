from datetime import timedelta

import flask_jwt_extended


class JWTGenerationManager:
    def __init__(self, access_expire_hour=2, refresh_expire_hour=48):
        """
        :param access_expire_hour: Access token expiration time in hours.
        :param refresh_expire_hour: Refresh token expiration time in hours.
        """
        self.access_expire_hour = access_expire_hour
        self.refresh_expire_hour = refresh_expire_hour

    def generate_token(self, user_id, custom_data=None, is_refresh=False):
        """
        Generate an access/refresh token with custom_data.

        :param user_id: The database id of the user for whom the token is generated.
        :param custom_data: Custom data to include in the token.
        :param is_refresh: Wheter to generate a refresh token or an access token
        :return: The generated access token.
        """

        additional_claims = {
            "custom_data": custom_data,
        }
        if is_refresh:
            expires = timedelta(hours=self.refresh_expire_hour)
            create_token = flask_jwt_extended.create_refresh_token
        else:
            expires = timedelta(hours=self.access_expire_hour)
            create_token = flask_jwt_extended.create_access_token

        return create_token(
            identity=user_id,
            expires_delta=expires,
            additional_claims=additional_claims
        )

    def generate_access_and_refresh_tokens(self, user_id, custom_data=None):
        return {
            "access_token": self.generate_token(user_id, custom_data, is_refresh=False),
            "refresh_token": self.generate_token(user_id, custom_data, is_refresh=True),
        }
