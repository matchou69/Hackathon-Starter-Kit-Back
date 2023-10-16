import os

from dotenv import load_dotenv

from shared import create_app

app = create_app()

if __name__ == "__main__":
    load_dotenv()
    if os.getenv("DEBUG") == "1":
        import debugpy

        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    app.run(host="0.0.0.0", port="5001", debug=True)
