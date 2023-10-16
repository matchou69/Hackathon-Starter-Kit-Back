from data.authentification.user.model import UserModel
from shared.authentification.schema_utils import PhoneNumberField
from shared.utils import BaseSchema


class UserSchema(BaseSchema):
    class Meta:
        model = UserModel
        load_instance = True

    phone = PhoneNumberField()
