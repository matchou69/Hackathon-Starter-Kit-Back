from data.hello_world.model import HelloWorldModel
from shared.utils.schema import BaseSchema


class HelloWorldSchema(BaseSchema):
    class Meta:
        model = HelloWorldModel
        load_instance = True
