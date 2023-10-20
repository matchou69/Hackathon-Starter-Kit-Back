import logging
import sys

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from errors import CustomError
from errors.database_errors import EntityNotFoundError

db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# image_manager: AssetImageManager = AssetImageManager(CLOUD_NAME, CLOUD_KEY, CLOUD_SECRET)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    print(f"Using {app.config['DB_NAME']}")
    print(app.config)

    url_prefix = "/api"

    db.init_app(app)
    jwt.init_app(app)
    if app.config["MIGRATION"] == "1":
        migrate.init_app(app, db)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    from data.hello_world import blueprint as hello_world_blueprint
    from data.authentification.password import password_blueprint
    from data.authentification.phone import blueprint as phone_auth_blueprint

    app.register_blueprint(hello_world_blueprint, url_prefix=url_prefix)
    app.register_blueprint(password_blueprint, url_prefix=url_prefix)
    app.register_blueprint(phone_auth_blueprint, url_prefix=url_prefix)

    @app.errorhandler(CustomError)
    @app.errorhandler(ValidationError)
    def handle_custom_error(error):
        return str(error), 400

    @app.errorhandler(EntityNotFoundError)
    def handle_not_found_error(error):
        return str(error), 404

    CORS(app, resources={r"/*": {"origins": "*"}})

    with app.app_context():
        db.create_all()
    return app
