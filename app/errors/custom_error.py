class CustomError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ModelError(CustomError):
    def __init__(self, message):
        super().__init__("Model Error : " + message)
