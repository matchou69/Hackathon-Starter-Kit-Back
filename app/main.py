from environment import GetAppEnvironment
from shared import create_app

environment = GetAppEnvironment.get()

print(f"Using environment {environment.ENV}")
app = create_app(environment)


if __name__ == "__main__":
    if environment.DEBUG:
        import debugpy

        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    app.run(host="0.0.0.0", port="5001", debug=True)
