""" Routes for the endpoint 'hello_world'"""

from flask import Blueprint, request
from marshmallow import ValidationError

from data.hello_world.models import HelloWorldModel
from data.hello_world.schemas import HelloWorldSchema
from shared import db

NAME = 'hello_world'

hello_world_blueprint = Blueprint(f"{NAME}_hello_world_blueprint", __name__)


@hello_world_blueprint.get(f"/hello_world/<int:id>")
def get_hello_world(id: str):
    """GET route code goes here"""
    entity: HelloWorldModel = db.session.query(HelloWorldModel).get(id)
    if entity is None:
        return "Goodby, World.", 404
    return entity.message, 200


@hello_world_blueprint.post(f"/hello_world/")
def post_hello_world():
    """POST route code goes here"""
    payload = request.get_json()
    try:
        entity: HelloWorldModel = HelloWorldSchema().load(payload)
    except ValidationError as error:
        return f"The payload does't correspond to a valid HelloWorldModel: {error}", 400
    db.session.add(entity)
    db.session.commit()
    return HelloWorldSchema().dump(entity), 200


@hello_world_blueprint.delete(f"/hello_world/<int:id>")
def delete_hello_world(id: str):
    """DELETE route code goes here"""
    return "Unimplemented", 501


@hello_world_blueprint.put(f"/hello_world/<int:id>")
def put_hello_world(id: str):
    """PUT route code goes here"""
    return "Unimplemented", 501


@hello_world_blueprint.patch(f"/hello_world/<int:id>")
def patch_hello_world(id: str):
    """PATCH route code goes here"""
    return "Unimplemented", 501
