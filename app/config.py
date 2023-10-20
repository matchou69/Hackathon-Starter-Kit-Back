from typing import Final

from dotenv import load_dotenv

from shared.utils.env_getter import EnvironmentGetter

load_dotenv()


class BaseConfig:
    """Configuration common to all modes (test, dev, prod)"""

    def __init__(self):
        self.env_getter = EnvironmentGetter()

        # Cloudinary
        # env_scope_coudinary = self.env_getter.scope("Cloudinary configuration (host and optimize media resources)")
        # self.CLOUD_NAME: Final[str] = env_scope_coudinary("CLOUD_NAME", "Cloudinary acount name", required=True)
        # self.CLOUD_KEY: Final[str] = env_scope_coudinary("CLOUD_KEY", "Cloudinary password", required=True)
        # self.CLOUD_SECRET: Final[str] = env_scope_coudinary("CLOUD_SECRET", "Cloudinary secret", required=True)

        # Twilio
        # env_scope_twilio = self.env_getter.scope("Twilio configuration (Phone authentication API)")
        # self.ACCOUNT_SID: Final[str] = env_scope_twilio.get("ACCOUNT_SID", "Twilio account id", required=True)
        # self.AUTH_TWILIO: Final[str] = env_scope_twilio.get("AUTH_TWILIO", "Twilio account password", required=True)

        # JWT
        env_scope_jwt = self.env_getter.scope("JWT configuration")
        self.JWT_SECRET_KEY: Final[str] = env_scope_jwt.get("JWT_SECRET",
                                                            "JWT secret key used for encryption/decryption of JWTs",
                                                            required=True)

        # Flask
        env_scope_migration = self.env_getter.scope("Flask configuration")
        self.MIGRATION: Final[str] = env_scope_migration.get("MIGRATION", "Whether to activate Flask-Migrate")

        # Database
        env_scope_database = self.env_getter.scope("Database configuration")
        self.USER: Final[str] = env_scope_database.get("DB_USER", "Name of the database user", required=True)
        self.DB_PASS: Final[str] = env_scope_database.get("DB_PASS", "Password of the database user", required=True)
        self.DB_NAME: Final[str] = env_scope_database.get("DB_NAME", "Name of the database", required=True)
        self.DB_IP: Final[str] = env_scope_database.get("DB_IP", "Adress of the database", required=True)
        self.SQLALCHEMY_DATABASE_URI: Final[str] = \
            f"postgresql://{self.USER}:{self.DB_PASS}@{self.DB_IP}:5432/{self.DB_NAME}"


class TestingConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.DEBUG = True
        self.ENV = "test"

        self.env_getter.fail_if_missing()


class DevelopmentConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.DEBUG = True
        self.ENV = "dev"

        self.env_getter.fail_if_missing()


class ProductionConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.DEBUG = False
        self.ENV = "prod"

        self.env_getter.fail_if_missing()
