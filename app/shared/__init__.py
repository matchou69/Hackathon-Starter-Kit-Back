import logging
import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    print(f"Using {app.config['DB_NAME']}")

    db.init_app(app)
    if app.config['MIGRATION'] == "1":
        migrate.init_app(app, db)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    url_prefix = "/api"

    """from data.hello_world.controllers import hello_world_blueprint
    app.register_blueprint(hello_world_blueprint, url_prefix=url_prefix)"""

    from data.auth.controllers import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix=url_prefix)
    from data.events.controllers import events_blueprint
    app.register_blueprint(events_blueprint, url_prefix=url_prefix)
    

    @app.errorhandler(ValidationError)
    def handle_custom_error(error):
        return str(error), 400

    CORS(app, resources={r"/*": {"origins": "*"}})

    with app.app_context():
        db.create_all()

    return app
