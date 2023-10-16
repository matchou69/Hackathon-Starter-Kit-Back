from marshmallow import fields, Schema


class LoginValidationSchema(Schema):
    phone = fields.String(required=True)
    code = fields.String(required=True)
