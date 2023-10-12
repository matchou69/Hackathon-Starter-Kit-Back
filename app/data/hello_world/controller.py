from flask import Blueprint, Response, request

from data.hello_world.model import HelloWorldModel
from data.hello_world.schema import HelloWorldSchema
from data.common import BaseCRUDHelper

name = 'helloworld'
blueprint = Blueprint(name + "_blueprint", __name__)

crud = BaseCRUDHelper(HelloWorldModel, HelloWorldSchema)


@blueprint.get('/' + name + "/<uuid:id>")
def get_hello_world(id):
    return crud.handle_get(id)


@blueprint.post('/' + name)
def post_hello_world():
    data = request.get_json()
    return crud.handle_post(data)
