import sqlalchemy
from sqlalchemy import Column, UUID, String

from shared import db


class UserModel(db.Model):
    __tablename__ = "user"
    id = Column(
        UUID, primary_key=True, unique=True, server_default=sqlalchemy.text("gen_random_uuid()"), nullable=False
    )
    username = Column(String)
    password = Column(String)
    phone = Column(String, unique=True)
