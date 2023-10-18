import sqlalchemy
from sqlalchemy import Column, UUID, String

from shared import db


class PhoneUserModel(db.Model):
    """Default user for phone authentification"""
    __tablename__ = "user_phone"
    id = Column(
        UUID, primary_key=True, unique=True, server_default=sqlalchemy.text("gen_random_uuid()"), nullable=False
    )
    username = Column(String)
    phone = Column(String, unique=True)

