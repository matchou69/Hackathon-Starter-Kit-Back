from werkzeug.security import generate_password_hash, check_password_hash
from shared import db

class UserModel(db.Model):
    __tablename__ = "user"
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

