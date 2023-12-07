"""Schema for serializing/deserializing a HelloWorldModel"""

from data.hello_world.models.hello_world_model import HelloWorldModel
from shared.utils.schema.base_schema import BaseSchema


class HelloWorldSchema(BaseSchema):
    class Meta:
        model = HelloWorldModel
        load_instance = True
