from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client as TwilioClient

from shared.authentification.errors import CustomTwilioError


class TwilioManager:
    def __init__(self, sid: str, auth: str):
        self.client = TwilioClient(sid, auth)

    def send_message(self, to: str, from_: str, body: str):
        try:
            self.client.messages.create(
                to=to,
                from_=from_,
                body=body
            )
        except TwilioRestException as twilio_error:
            raise CustomTwilioError(twilio_error)
