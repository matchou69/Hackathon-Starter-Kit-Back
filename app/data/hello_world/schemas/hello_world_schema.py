from data.hello_world.models.hello_world_model import HelloWorldModel
from shared.utils.schema import BaseSchema


class HelloWorldSchema(BaseSchema):
    class Meta:
        model = HelloWorldModel
        load_instance = True
