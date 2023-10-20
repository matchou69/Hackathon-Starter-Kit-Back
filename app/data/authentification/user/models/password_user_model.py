import sqlalchemy

from shared import db


class PasswordUserModel(db.Model):
    """Default user for password authentification"""
    __tablename__ = "user_password"
    id = db.Column(
        db.UUID, primary_key=True, unique=True, server_default=sqlalchemy.text("gen_random_uuid()"), nullable=False
    )
    username = db.Column(db.String)
    password = db.Column(db.String)
    mail = Column(db.String, unique=True)
