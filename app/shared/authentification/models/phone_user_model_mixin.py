import sqlalchemy
from sqlalchemy import Column, UUID, String

from shared import db


class PhoneUserModelMixin:
    phone = Column(String(255), nullable=False, unique=True)
