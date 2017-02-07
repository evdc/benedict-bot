import logging
logging.basicConfig(level='INFO')
log = logging.Logger(__name__)

from flask import Flask, request
from intent_classifier.model import Model

m = Model()
server = Flask(__name__)

@server.route("/", methods=['POST'])
def parse():
	json_ = request.get_json(force=True)
	log.info("Received JSON: ", json_)
	message = json_["message"]
	res = m(message, {})
	return res['response']

if __name__ == "__main__":
	server.run()