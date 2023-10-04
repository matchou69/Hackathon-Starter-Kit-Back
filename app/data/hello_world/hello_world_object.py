from graphene_sqlalchemy import SQLAlchemyObjectType

from data.hello_world.hello_world_model import HelloWorldModel


class HelloWorldObject(SQLAlchemyObjectType):
    class Meta:
        model = HelloWorldModel
