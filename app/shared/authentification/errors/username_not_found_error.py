from errors import CustomError


class UsernameNotFoundError(CustomError):
    def __init__(self, name):
        message = f"Username not found: {name}"
        super().__init__(message)
