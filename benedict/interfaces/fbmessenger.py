from flask import jsonify, make_response, request
from flask_restful import Resource
import json
import requests

VERIFY_TOKEN = "Q1W2E3R4T5"
PAGE_ACCESS_TOKEN = "EAAFr6jlzGY4BAHVGqfY4zZBrcij50MKph5leBhi0YAEy3OZBlZCsineDirk5ZBP2OXQWFSIyhRaGXPazTOX0r7bZBnpFm0DshoONWpgWZCTxNcZAU9t5eEWojnctlBypGpxVPdCjZAdpKuHvexNnuUOUeUZBf9n5n18tv4RsZCFj8PKAZDZD"

GRAPH_URL = "https://graph.facebook.com/v2.6"


class FbMessengerWebhook(Resource):
    def __init__(self, **kwargs):
        self.engine = kwargs['engine']
        self.debug = kwargs.get('debug', False)

    def get(self):
        """Respond to status requests from Facebook."""
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
                return make_response("Verification token mismatch", 403)
            return make_response(request.args["hub.challenge"], 200)
        return make_response("Hello World", 200)

    def post(self):
        data = request.get_json()
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        recipient_id = messaging_event["recipient"]["id"]
                        message_text = messaging_event["message"]["text"]

                        # Respond. Do try not to block here.
                        response = self.engine.handle_message({
                            'user': sender_id,
                            'text': message_text
                        })
                        if self.debug:
                            return {"response": response}, 200
                        send_message(sender_id, response)

        return "ok", 200


def send_message(recipient_id, message_text):
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    print("SENDING MESSAGE {} to {}".format(message_text, recipient_id))
    r = requests.post("{}/me/messages".format(GRAPH_URL), params=params, headers=headers, data=data)
