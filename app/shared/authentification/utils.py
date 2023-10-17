from datetime import timedelta

from flask_jwt_extended import create_access_token, create_refresh_token


def generate_token(user, custom_data, duration_hour):
    """
    Generate an access token with additional data.

    :param user: The user for whom the token is generated.
    :param custom_data: Custom data to include in the token.
    :param duration_hour: Token expiration time in hours.
    :return: The generated access token.
    """

    expires = timedelta(hours=duration_hour)
    additional_claims = {
        "custom_data": custom_data,
    }
    access_token = create_access_token(identity=user, expires_delta=expires, additional_claims=additional_claims)
    return access_token


def generate_refresh_token(user, custom_data, duration_day):
    expires = timedelta(days=duration_day)
    additional_claims = {
        "custom_data": custom_data,
    }
    access_token = create_refresh_token(identity=user, expires_delta=expires, additional_claims=additional_claims)
    return access_token
