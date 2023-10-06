import graphene

from errors import CustomError
from errors import IdAlreadySetError
from shared import db
from data.utils import input_to_dictionary, is_id_usable


class BaseCreateMutation(graphene.Mutation):
    """
    Base mutation for creating data in the database.

    This class simplifies the process of creating data in the database using GraphQL mutations and SQLAlchemy.

    Args:
        input (graphene.InputObjectType): The input object containing data to create.

    Attributes:
        input (graphene.InputObjectType): The input object containing data to create.

    Methods:
        - `mutate(cls, root, info, input)`: The core method for creating data in the database.
        - `get_model_class(cls)`: Subclasses must implement this method to specify the model class for data creation.
        - `post_process_data(cls, data)`: Optional method for additional data processing after extraction.

    Example Usage:
        class CreateUserMutation(BaseCreateMutation):
            # ...

    """
    class Arguments:
        input = graphene.InputObjectType()

    @classmethod
    def mutate(cls, root, info, input):
        """
        Create data in the database.

        Args:
            root: The root query object.
            info: Information about the GraphQL execution.
            input: The input data to create.

        Returns:
            cls: An instance of the mutation class with the created data.

        Raises:
            IdAlreadySetError: If the provided ID is already set in the data.

        """
        data = input_to_dictionary(input)
        model_class = cls.get_model_class()

        if is_id_usable(data.get("id"), model_class):
            raise IdAlreadySetError(cls.__name__, model_class, data["id"])

        cls.post_process_data(data)
        create_element = model_class(**data)

        db.session.add(create_element)
        db.session.flush()
        db.session.commit()

        return cls(create_element)

    @classmethod
    def get_model_class(cls):
        """
           Get the SQLAlchemy model class for data creation.

           Subclasses must implement this method to specify the model class for data creation.

           Returns:
               sqlalchemy.Model: The SQLAlchemy model class.

           Raises:
               NotImplementedError: Subclasses must implement this method.

           """
        raise NotImplementedError("Subclasses must implement get_model_class method.")

    @classmethod
    def post_process_data(cls, data):
        """
        Optional data processing after data extraction.

        Args:
            data (dict): The extracted data.

        """
        pass
