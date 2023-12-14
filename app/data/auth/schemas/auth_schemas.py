from data.auth.models.auth_models import UserModel
from shared.utils.schema.base_schema import BaseSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE

class UserSchema(BaseSchema):
    class Meta:
        model = UserModel
        load_instance = True
        unknown = EXCLUDE