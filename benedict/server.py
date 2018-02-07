from flask import Flask, request, jsonify
from flask_restful import Api

from interfaces.fbmessenger import FbMessengerWebhook
from core import Engine

def create_server(env='Test'):
	app = Flask(__name__)
	api = Api()
	engine = Engine()

	api.add_resource(FbMessengerWebhook, "/fbmsg", 
		resource_class_kwargs={'engine': engine})

	api.init_app(app)

	return app

server = create_server(None)

if __name__ == "__main__":
	server.run(debug=True)