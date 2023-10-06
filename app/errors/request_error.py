from errors.custom_error import ModelError

class TypeMismatchError(ModelError):
    """
    Error indicating a type mismatch between a data type and a cluster type.

    This error is raised when there is a type mismatch between the expected data type and the cluster type.

    Args:
        classname (str): The name of the class where the error occurred.
        data_type (str): The data type that caused the mismatch.
        cluster_type (str): The cluster type expected.

    Example Usage:
        try:
            # Code that may raise TypeMismatchError
        except TypeMismatchError as e:
            print(e)

    """
    def __init__(self, classname, data_type, cluster_type):
        message = (
            f"on {classname} the type '{data_type}' "
            f"doesn't match with the cluster type: '{cluster_type}'"
        )
        super().__init__(message)

class IdNotFoundError(ModelError):
    """
    Error indicating that an ID was not found in the database table.

    This error is raised when an ID is not found in the specified database table.

    Args:
        classname (str): The name of the class where the error occurred.
        model_class: The SQLAlchemy model class representing the database table.
        id: The ID that was not found.

    Example Usage:
        try:
            # Code that may raise IdNotFoundError
        except IdNotFoundError as e:
            print(e)

    """
    def __init__(self, classname, model_class, id):
        message = (
            f"on {classname} id not found in the table "
            f"'{model_class.__tablename__}': {id}"
        )
        super().__init__(message)

class IdAlreadySetError(ModelError):
    """
    Error indicating that an ID is already set in the database table.

    This error is raised when an attempt is made to set an ID that already exists in the specified database table.

    Args:
        classname (str): The name of the class where the error occurred.
        model_class: The SQLAlchemy model class representing the database table.
        id: The ID that is already set.

    Example Usage:
        try:
            # Code that may raise IdAlreadySetError
        except IdAlreadySetError as e:
            print(e)

    """
    def __init__(self, classname, model_class, id):
        message = (
            f"on {classname} id already set in the table "
            f"'{model_class.__tablename__}': {id}"
        )
        super().__init__(message)
