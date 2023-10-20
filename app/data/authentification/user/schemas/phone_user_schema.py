from data.authentification.user.models.phone_user_model import PhoneUserModel as UserModel
from shared.authentification.schema_utils import PhoneNumberField
from shared.utils.schema import BaseSchema


class UserSchema(BaseSchema):
    class Meta:
        model = UserModel
        load_instance = True

    phone = PhoneNumberField()
