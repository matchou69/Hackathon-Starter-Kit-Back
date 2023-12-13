from sqlalchemy import Column, String, Integer , Date
from sqlalchemy.sql import func
from shared import db
from werkzeug.security import generate_password_hash, check_password_hash


class EventsModel(db.Model):
    __tablename__ = "events"
    id = db.Column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False
    )
    name = db.Column(String(100))
    photo = db.Column(String(200))
    description = db.Column(String(1000))
    date = db.Column (Date)

