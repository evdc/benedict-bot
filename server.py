from flask import Flask, request, jsonify
from flask_restful import Api

from interfaces.fbmessenger import FbMessengerWebhook

def create_server():
	server = Flask(__name__)
	api = Api()

	api.add_resource(FbMessengerWebhook, "/fbmsg")

	api.init_app(server)

	return server

server = create_server()

if __name__ == "__main__":
	server.run(debug=True)