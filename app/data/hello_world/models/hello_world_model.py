import sqlalchemy

from shared import db
from sqlalchemy import Column, UUID, String, Integer


class HelloWorldModel(db.Model):
    __tablename__ = "hello_world"
    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False
    )
    message = Column(String(100))
