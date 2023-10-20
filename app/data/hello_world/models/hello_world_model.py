import sqlalchemy
from sqlalchemy import Column, UUID, String

from shared import db


class HelloWorldModel(db.Model):
    __tablename__ = "helloworld"
    id = Column(
        UUID, primary_key=True, unique=True, server_default=sqlalchemy.text("gen_random_uuid()"), nullable=False
    )
    name = Column(String())
