import os

from dotenv import load_dotenv

from shared.utils.env_getter import EnvironmentGetter


class BaseEnvironment:
    """Configuration common to all modes (test, dev, prod)"""

    def __init__(self):
        self.env_getter = EnvironmentGetter()

        # Flask
        env_scope_migration = self.env_getter.scope("Flask configuration")
        self.MIGRATION: str = env_scope_migration.get("MIGRATION", "Whether to activate Flask-Migrate")

        # Database
        env_scope_database = self.env_getter.scope("Database configuration")
        self.USER: str = env_scope_database.get("DB_USER", "Name of the database user", required=True)
        self.DB_PASS: str = env_scope_database.get("DB_PASS", "Password of the database user", required=True)
        self.DB_NAME: str = env_scope_database.get("DB_NAME", "Name of the database", required=True)
        self.DB_IP: str = env_scope_database.get("DB_IP", "Adress of the database", required=True)
        self.SQLALCHEMY_DATABASE_URI: str = \
            f"postgresql://{self.USER}:{self.DB_PASS}@{self.DB_IP}:5432/{self.DB_NAME}"

        # Defaults
        self.DEBUG: bool = False
        self.ENV: str = ""

    def fail_if_missing(self):
        self.env_getter.fail_if_missing()

class TestingEnvironment(BaseEnvironment):
    def __init__(self):
        super().__init__()
        self.DEBUG = True
        self.ENV = "test"


class DevelopmentEnvironment(BaseEnvironment):
    def __init__(self):
        super().__init__()
        self.DEBUG = True
        self.ENV = "dev"


class ProductionEnvironment(BaseEnvironment):
    def __init__(self):
        super().__init__()
        self.DEBUG = False
        self.ENV = "prod"


class GetAppEnvironment:
    _loaded_environment: BaseEnvironment | None = None

    @classmethod
    def get(cls) -> BaseEnvironment:
        if cls._loaded_environment is not None:
            return cls._loaded_environment

        load_dotenv()
        environment_mode = os.getenv("ENV")
        if environment_mode is None:
            environment_mode = "dev"
        if environment_mode == "test":
            environment = TestingEnvironment()
        elif environment_mode == "prod":
            environment = ProductionEnvironment()
        elif environment_mode == "dev" or os.getenv("ENV") is None:
            environment = DevelopmentEnvironment()
        else:
            raise Exception("Missing or incorrect 'ENV'. Possible values: test | prod | dev (default: dev)")
        environment.fail_if_missing()

        cls._loaded_environment = environment
        return cls._loaded_environment
