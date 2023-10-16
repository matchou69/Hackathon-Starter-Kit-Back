import sqlalchemy

from shared import db


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(
        db.UUID, primary_key=True, unique=True, server_default=sqlalchemy.text("gen_random_uuid()"), nullable=False
    )
    username = db.Column(db.String)
    password = db.Column(db.String)
    phone = db.Column(db.String, unique=True)
