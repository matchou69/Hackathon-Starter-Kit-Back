import graphene

from data.hello_world.hello_world_model import HelloWorldModel
from data.hello_world.hello_world_object import HelloWorldObject
from data.mutation_utils import BaseCreateMutation


class CreateHelloWorldInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class CreateHelloWorld(BaseCreateMutation):
    class Arguments:
        input = CreateHelloWorldInput()

    hello_world = graphene.Field(lambda: HelloWorldObject)

    @classmethod
    def get_model_class(cls):
        return HelloWorldModel

    @classmethod
    def post_process_data(cls, data):
        data['id'] = 1
