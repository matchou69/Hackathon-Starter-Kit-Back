import re

import bcrypt
from marshmallow import fields, ValidationError


class PasswordField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
