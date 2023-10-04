import graphene

from data.hello_world import CreateHelloWorld
from data.hello_world.hello_world_resolver import HelloWorldResolver


class Mutation(graphene.ObjectType):
    create_hello_world = CreateHelloWorld.Field()


class Query(graphene.ObjectType, HelloWorldResolver):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)