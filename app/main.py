import os

from dotenv import load_dotenv
from flask_graphql import GraphQLView

from schema import schema
from shared import create_app

app = create_app()
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
    ),
)

if __name__ == "__main__":
    load_dotenv()
    if os.getenv("DEBUG") == "1":
        import debugpy

        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    app.run(host="0.0.0.0", port="5001", debug=True)