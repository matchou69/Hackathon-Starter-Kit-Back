import sqlalchemy
from sqlalchemy import Column, UUID, String

from shared.authentification.models.password_user_model_mixin import PasswordUserModelMixin
from shared.authentification.models.phone_user_model_mixin import PhoneUserModelMixin
from shared import db


class UserModel(db.Model, PhoneUserModelMixin, PasswordUserModelMixin):
    __tablename__ = "user"
    id = Column(
        UUID, primary_key=True, unique=True, server_default=sqlalchemy.text("gen_random_uuid()"), nullable=False
    )
    username = Column(String(255), nullable=False, unique=True)
