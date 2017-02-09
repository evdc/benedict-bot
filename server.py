from flask import Flask, request, jsonify
from intent_classifier.main import IntentClassifier

intent_classifier = IntentClassifier()
server = Flask(__name__)

@server.route("/", methods=['POST'])
def parse():
	json_ = request.get_json(force=True)
	log.info("Received JSON: ", json_)
	message = json_["message"]
	res = intent_classifier(message, {})
	return jsonify(res)

if __name__ == "__main__":
	server.run()