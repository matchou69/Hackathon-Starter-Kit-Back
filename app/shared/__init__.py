import logging
import os
import sys
from typing import Final

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from shared.cloudinary.asset_image_manager import AssetImageManager

load_dotenv()
ENV: Final[str] = os.getenv("ENV")
USER: Final[str] = os.getenv("DB_USER")
DB_PASS: Final[str] = os.getenv("DB_PASS")
# db_dev si dev envs, db_qual si c'est prod, db_test si tester
DB_NAME: Final[str] = os.getenv("DB_NAME")
DB_IP: Final[str] = os.getenv("DB_IP")
MIGRATION: Final[str] = os.getenv("MIGRATION")

JWT_SECRET: Final[str] = os.getenv("JWT_SECRET")
if JWT_SECRET is None:
    raise Exception("JWT_SECRET is not defined in the .env file")

db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
#image_manager: AssetImageManager = AssetImageManager(CLOUD_NAME, CLOUD_KEY, CLOUD_SECRET)


def create_app():
    app = Flask(__name__)
    print(f"Using {DB_NAME}")
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql://{USER}:{DB_PASS}@{DB_IP}:5432/{DB_NAME}"
    app.config["JWT_SECRET_KEY"] = JWT_SECRET

    url_prefix = '/api'

    db.init_app(app)
    jwt.init_app(app)
    if MIGRATION == "1":
        migrate.init_app(app, db)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    from data.hello_world import blueprint as hello_world_blueprint
    from data.authentification import blueprint as auth_blueprint
    app.register_blueprint(hello_world_blueprint, url_prefix=url_prefix)
    app.register_blueprint(auth_blueprint, url_prefix=url_prefix)

    CORS(app, resources={r"/*": {"origins": "*"}})

    with app.app_context():
        db.create_all()
    return app
