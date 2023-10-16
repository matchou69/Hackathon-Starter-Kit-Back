from errors import CustomError


class IncorrectVerificationCodeError(CustomError):
    def __init__(self):
        message = f"Incorrect verification code"
        super().__init__(message)
