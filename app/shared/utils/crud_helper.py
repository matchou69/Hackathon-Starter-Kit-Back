from shared.utils.registry import Registry
from shared.utils.schema import BaseSchema


class BaseCRUDHelper:
    """Utility class for basic CRUD operations on an SQLAlchemy data model."""

    def __init__(self, model: type, schema: BaseSchema):
        self.schema = schema
        self.model = model
        self.name = self.model.__tablename__
        self.registry = Registry(model)

    def handle_get(self, id):
        entity = self.registry.get_by_id(id)
        return_value = self.schema.dump(entity)
        return return_value, 200

    def handle_delete(self, id):
        self.registry.delete_by_id(id)
        return {"message": 'success'}, 200

    def handle_put(self, id, data):
        entity = self.registry.get_by_id(id)
        self.schema.load(data, instance=entity, partial=True)
        self.registry.save_entity(entity)
        return self.schema.dump(entity), 200

    def handle_post(self, data):
        entity = self.schema.load(data)
        self.registry.save_entity(entity)
        return {'id': entity.id, 'status': 'success'}, 201
