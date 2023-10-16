import re
from marshmallow import fields, ValidationError


class PhoneNumberField(fields.Field):
    phone_pattern = re.compile(r"((\+330?)|0)(?P<digits>\d{9})")

    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        match = PhoneNumberField.phone_pattern.fullmatch(value)
        if match is None:
            raise ValidationError(f"Invalid Phone Number: {value}")
        print(f"+33{match['digits']}", flush=True)
        return f"+33{match['digits']}"
