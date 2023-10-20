from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from data.hello_world.models.hello_world_model import HelloWorldModel
from data.hello_world.schemas.hello_world_schema import HelloWorldSchema
from shared.utils.crud_helper import BaseCRUDHelper

NAME = "helloworld"
blueprint = Blueprint(f"{NAME}_blueprint", __name__)

crud = BaseCRUDHelper(HelloWorldModel, HelloWorldSchema())


@blueprint.get(f"/{NAME}/<uuid:id>")
def get_hello_world(id):
    return crud.handle_get(id)


@blueprint.post(f"/{NAME}/")
def post_hello_world():
    data = request.get_json()
    return crud.handle_post(data)


@blueprint.delete(f"/{NAME}/<uuid:id>")
def delete_hello_world(id):
    return crud.handle_delete(id)


@blueprint.put(f"/{NAME}/<uuid:id>")
@jwt_required()
def update_hello_world(id):
    current_user = get_jwt_identity()
    print(current_user + " - " + get_jwt()["custom_data"], flush=True)
    data = request.get_json()
    return crud.handle_put(id, data)
