from data.hello_world.model import HelloWorldModel
from shared.utils import BaseSchema


class HelloWorldSchema(BaseSchema):
    class Meta:
        model = HelloWorldModel
        load_instance = True
