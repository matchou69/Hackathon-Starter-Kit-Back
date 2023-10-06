import logging
import os
import sys
from typing import Final

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


load_dotenv()
ENV: Final[str] = os.getenv("ENV")
USER: Final[str] = os.getenv("DB_USER")
DB_PASS: Final[str] = os.getenv("DB_PASS")
DB_NAME: Final[str] = os.getenv("DB_NAME")
DB_IP: Final[str] = os.getenv("DB_IP")
MIGRATION: Final[str] = os.getenv("MIGRATION")
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    print(f"Using {DB_NAME}")
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql://{USER}:{DB_PASS}@{DB_IP}:5432/{DB_NAME}"

    db.init_app(app)
    if MIGRATION == "1":
        migrate.init_app(app, db)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    CORS(app, resources={r"/*": {"origins": "*"}})

    with app.app_context():
        db.create_all()
    return app
