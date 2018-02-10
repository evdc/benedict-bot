from flask import Flask, request, jsonify
from flask_restful import Api

from benedict.interfaces.fbmessenger import FbMessengerWebhook
from benedict.core import Engine

def create_app(env='Test'):
	app = Flask(__name__)
	api = Api()
	engine = Engine()

	api.add_resource(FbMessengerWebhook, "/fbmsg", 
		resource_class_kwargs={'engine': engine})

	api.init_app(app)

	return app