from shared.authentification.model.user_model import UserModel
from shared.utils import BaseSchema


class UserSchema(BaseSchema):
    class Meta:
        model = UserModel
        load_instance = True
