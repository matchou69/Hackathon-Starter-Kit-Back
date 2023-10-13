import sqlalchemy

from shared import db


class HelloWorldModel(db.Model):
    __tablename__ = "helloworld"
    id = db.Column(
        db.UUID, primary_key=True, unique=True, server_default=sqlalchemy.text("gen_random_uuid()"), nullable=False
    )
    name = db.Column(db.String())
