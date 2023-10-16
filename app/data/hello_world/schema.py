from marshmallow import fields

from data.hello_world.model import HelloWorldModel
from data.common import BaseSchema


class HelloWorldSchema(BaseSchema):
    class Meta:
        model = HelloWorldModel
        load_instance = True