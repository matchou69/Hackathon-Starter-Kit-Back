from shared import create_app
import os
from dotenv import load_dotenv
from config import TestingConfig, ProductionConfig, DevelopmentConfig
from flask_cors import CORS

load_dotenv()


match os.getenv('ENV'):
    case 'dev':
        config = DevelopmentConfig()
    case 'prod':
        config = ProductionConfig()
    case 'test':
        config = TestingConfig()
    case _:
        config = DevelopmentConfig()

print(f"Using environment {config.ENV}")

app = create_app(config)
CORS(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001", debug=True)
