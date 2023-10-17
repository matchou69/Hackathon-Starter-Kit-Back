from errors import CustomError


class EntityNotFoundError(CustomError):
    def __init__(self, model, **kwargs):
        search_that_failed = ", ".join(f"{criterion}={value}" for criterion, value in kwargs.items())
        message = f"{model.__table__} not found for {search_that_failed}"
        super().__init__(message)


class MultipleResultsFoundError(CustomError):
    def __init__(self, model, **kwargs):
        search_that_failed = ", ".join(f"{criterion}={value}" for criterion, value in kwargs.items())
        message = f"Asked for only one {model.__table__} but multiple were foun for {search_that_failed}"
        super().__init__(message)
