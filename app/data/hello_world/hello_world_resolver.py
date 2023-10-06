import graphene

from data.hello_world.hello_world_model import HelloWorldModel
from data.hello_world.hello_world_object import HelloWorldObject
from shared import db


class HelloWorldResolver:
    hello_world = graphene.List(HelloWorldObject)

    def resolve_hello_world(self, info):
        return db.session.query(HelloWorldModel).all()