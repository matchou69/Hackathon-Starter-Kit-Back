from sqlalchemy import Column, String, Integer

from shared import db


class HelloWorldModel(db.Model):
    __tablename__ = "hello_world"
    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False
    )
    message = Column(String(100))
