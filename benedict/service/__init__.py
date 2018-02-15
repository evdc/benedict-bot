from flask import Flask, request, jsonify
from flask_restful import Api
from celery import Celery

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

def setup_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.config_from_object('benedict.config.celeryconfig')
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery