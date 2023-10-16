from marshmallow import Schema, fields


class LoginValidationSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
