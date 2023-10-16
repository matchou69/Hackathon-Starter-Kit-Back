from errors import CustomError


class CustomTwilioError(CustomError):
    def __init__(self, twilio_error):
        message = f"Error with the Twilio REST API: {twilio_error}"
        super().__init__(message)
