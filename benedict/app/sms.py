from twilio.rest import Client
import os

ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']


def send_message(body, to, from_=PHONE_NUMBER):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    print("Sending message {} to {}".format(body, to))
    message = client.messages.create(
        from_=from_,
        to=to,
        body=body
    )
