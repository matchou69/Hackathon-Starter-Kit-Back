import sqlalchemy.exc

from shared import db
from errors.database_errors import EntityNotFoundError, MultipleResultsFoundError


class Registry:
    """
    Wrapper around database related calls with remap to custom errors
    """

    def __init__(self, model):
        self.model = model
        self.name = self.model.__tablename__

    def save_entity(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity

    def delete_entity(self, entity):
        db.session.delete(entity)
        db.session.commit()

    def delete_by_id(self, id):
        entity = self.get_by_id(id)
        db.session.delete(entity)
        db.session.commit()

    def get_by_id(self, id):
        return db.session.get(self.model, id, with_for_update=True)

    def get_all_where(self, **kwargs):
        # TODO erreur si un kwarg n'est pas une colonne
        return db.session.query(self.model).filter_by(**kwargs).all()

    def get_one_or_fail_where(self, **kwargs):
        try:
            result = db.session.query(self.model).filter_by(**kwargs).one_or_none()
            if result is None:
                raise EntityNotFoundError(self.model, **kwargs)
            return result
        except sqlalchemy.exc.MultipleResultsFound:
            raise MultipleResultsFoundError(self.model, **kwargs)
