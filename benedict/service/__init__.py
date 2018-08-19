from flask import Flask
from flask_restful import Api

from benedict.interfaces.fbmessenger import FbMessengerWebhook
from benedict.core.engine import Engine


def create_app(env='Test'):
    app = Flask(__name__)
    api = Api()
    engine = Engine()

    app.config.from_object('benedict.config.config.{}Config'.format(env))

    api.add_resource(FbMessengerWebhook, "/fbmsg",
                     resource_class_kwargs={'engine': engine, 'debug': app.config['DEBUG']})

    api.init_app(app)

    return app

