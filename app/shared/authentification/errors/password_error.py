from errors import CustomError


class WrongPasswordError(CustomError):
    def __init__(self):
        message = "Wrong password"
        super().__init__(message)
