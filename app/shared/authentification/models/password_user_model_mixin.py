import sqlalchemy
from sqlalchemy import Column, UUID, String

from shared import db


class PasswordUserModelMixin:
    password = Column(String(255), nullable=False)
    mail = Column(String(255), nullable=False, unique=True)
