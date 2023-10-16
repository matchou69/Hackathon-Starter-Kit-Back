from errors import CustomError


class UserNotFoundException(CustomError):
    def __init__(self, **kwargs):
        search_that_failed = ", ".join(f"{criterion}={value}" for criterion, value in kwargs.items())
        message = f"User not found for {search_that_failed}"
        super().__init__(message)
