import os

from dotenv import load_dotenv

from config import TestingConfig, ProductionConfig, DevelopmentConfig
from shared import create_app

load_dotenv()
if os.getenv("ENV") == "test":
    config = TestingConfig()
elif os.getenv("ENV") == "prod":
    config = ProductionConfig()
elif os.getenv("ENV") == "dev" or os.getenv("ENV") is None:
    config = DevelopmentConfig()
else:
    raise Exception("Missing environment variable named ENV (possible values): test | prod | dev (default: dev)")
print(f"Using environment {config.ENV}")

app = create_app(config)

if __name__ == "__main__":
    load_dotenv()
    if os.getenv("DEBUG") == "1":
        import debugpy

        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    app.run(host="0.0.0.0", port="5001", debug=True)
