from flask import Blueprint, Response, request

from data.hello_world.model import HelloWorldModel
from data.hello_world.schema import HelloWorldSchema
from data.common import BaseCRUDHelper

NAME = 'helloworld'
blueprint = Blueprint(NAME + "_blueprint", __name__)

crud = BaseCRUDHelper(HelloWorldModel, HelloWorldSchema())


@blueprint.get('/' + NAME + "/<uuid:id>")
def get_hello_world(id):
    return crud.handle_get(id)


@blueprint.post('/' + NAME)
def post_hello_world():
    data = request.get_json()
    return crud.handle_post(data)


@blueprint.delete('/' + NAME + "/<uuid:id>")
def delete_hello_world(id):
    return crud.handle_delete(id)


@blueprint.put('/' + NAME + "/<uuid:id>")
def update_heelo_world(id):
    data = request.get_json()
    return crud.handle_put(id, data)
