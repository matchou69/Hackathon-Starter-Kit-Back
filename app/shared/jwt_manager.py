from datetime import timedelta

from flask import request, jsonify
from flask_jwt_extended import create_access_token


def generate_token(user, additional_data, hour):
    expires = timedelta(hours=hour)
    additional_claims = {
        "custom_data": additional_data,
    }
    access_token = create_access_token(identity=user, expires_delta=expires, additional_claims=additional_claims)
    return access_token
