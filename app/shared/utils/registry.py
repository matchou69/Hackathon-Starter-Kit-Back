from typing import TypeVar, Generic, Callable, List

import sqlalchemy.exc

from errors.database_errors import EntityNotFoundError, MultipleResultsFoundError
from shared import db

ModelType = TypeVar('ModelType')


class Registry(Generic[ModelType]):
    """
    Wrapper around database related calls with remap to custom errors
    """

    def __init__(self, model: Callable[[...], ModelType]):
        self.model = model
        self.name = self.model.__tablename__

    def save_entity(self, entity: ModelType) -> ModelType:
        db.session.add(entity)
        db.session.commit()
        return entity

    def delete_entity(self, entity: ModelType):
        db.session.delete(entity)
        db.session.commit()

    def delete_by_id(self, id: str):
        entity = self.get_by_id(id)
        db.session.delete(entity)
        db.session.commit()

    def get_by_id(self, id: str) -> ModelType | None:
        return db.session.get(self.model, id, with_for_update=True)

    def get_by_id_or_fail(self, id: str) -> ModelType:
        result = self.get_by_id(id)
        if result is None:
            raise EntityNotFoundError(self.model)
        return result

    def get_all_where(self, **kwargs) -> List[ModelType]:
        # TODO erreur si un kwarg n'est pas une colonne
        return db.session.query(self.model).filter_by(**kwargs).all()

    def get_one_or_fail_where(self, **kwargs) -> ModelType:
        try:
            result = db.session.query(self.model).filter_by(**kwargs).one_or_none()
            if result is None:
                raise EntityNotFoundError(self.model, **kwargs)
            return result
        except sqlalchemy.exc.MultipleResultsFound:
            raise MultipleResultsFoundError(self.model, **kwargs)
