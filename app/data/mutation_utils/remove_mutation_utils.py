import copy
import graphene
from errors import IdNotFoundError
from shared import db
from data.utils import input_to_dictionary


class RemoveDefaultInput:
    """
    Input object for removing an element with a specified ID.

    Attributes:
        id (graphene.ID): The ID of the element to remove (required).

    Example Usage:
        input = RemoveDefaultInput()
    """

    id = graphene.ID(required=True)


class BaseRemoveMutation(graphene.Mutation):
    """
    Base mutation for removing an element from the database.

    This class simplifies the process of removing data from the database using GraphQL mutations and SQLAlchemy.

    Methods:
        - `mutate(cls, root, info, input)`: The core method for removing data from the database.
        - `get_model_class(cls)`: Subclasses must implement this method to specify the model class for data removal.

    Example Usage:
        class RemoveUserMutation(BaseRemoveMutation):
            # ...

    """

    class Arguments:
        input = graphene.InputObjectType()

    @classmethod
    def mutate(cls, root, info, input):
        """
        Remove data from the database.

        Args:
            root: The root query object.
            info: Information about the GraphQL execution.
            input: The input data specifying the ID of the element to remove.

        Returns:
            cls: An instance of the mutation class with the removed element.

        Raises:
            IdNotFoundError: If the provided ID is not found in the database.

        """
        data = input_to_dictionary(input)
        model_class = cls.get_model_class()
        remove_element = copy.copy(db.session.query(model_class).get(data["id"]))
        if remove_element is None:
            raise IdNotFoundError(cls.__name__, model_class, data["id"])
        db.session.query(model_class).filter_by(id=data["id"]).delete()
        db.session.flush()
        db.session.commit()

        return cls(remove_element)

    @classmethod
    def get_model_class(cls):
        """
        Get the SQLAlchemy model class for data removal.

        Subclasses must implement this method to specify the model class for data removal.

        Returns:
            sqlalchemy.Model: The SQLAlchemy model class.

        Raises:
            NotImplementedError: Subclasses must implement this method.

        """
        raise NotImplementedError("Subclasses must implement get_model_class method.")
