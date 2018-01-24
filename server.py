from flask import Flask, request, jsonify
import requests
import json

server = Flask(__name__)

VERIFY_TOKEN = "Q1W2E3R4T5"
PAGE_ACCESS_TOKEN = "EAAFr6jlzGY4BAHVGqfY4zZBrcij50MKph5leBhi0YAEy3OZBlZCsineDirk5ZBP2OXQWFSIyhRaGXPazTOX0r7bZBnpFm0DshoONWpgWZCTxNcZAU9t5eEWojnctlBypGpxVPdCjZAdpKuHvexNnuUOUeUZBf9n5n18tv4RsZCFj8PKAZDZD"

@server.route("/", methods=['GET'])
def verify():
	"""Respond to status requests from Facebook."""
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello World", 200

@server.route("/", methods=['POST'])
def handle_fb_message():
	data = request.get_json()
	print "Received JSON:", data
	if data["object"] == "page":
		for entry in data["entry"]:
			for messaging_event in entry["messaging"]:
				if messaging_event.get("message"):
					sender_id = messaging_event["sender"]["id"]
					recipient_id = messaging_event["recipient"]["id"]
					message_text = messaging_event["message"]["text"]

					# Respond
					send_message(sender_id, "You just said {}.".format(message_text))

				if messaging_event.get("delivery"):
					pass	# delivery confirmation

				if messaging_event.get("optin"):
					pass

				if messaging_event.get("postback"):
					pass

	return "ok", 200

def send_message(recipient_id, message_text):
	graph_url = "https://graph.facebook.com/v2.6"
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
	r = requests.post("{}/me/messages".format(graph_url), params=params, headers=headers, data=data)
	if r.status_code != 200:
		print r.status_code, r.text

if __name__ == "__main__":
	server.run(debug=True)