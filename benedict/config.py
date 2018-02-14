import os

from celery.schedules import crontab

class Config(object):
	DEBUG = False
	TESTING = False

class TestConfig(Config):
	DEBUG = True
	TESTING = True

class ProductionConfig(Config):
	pass

class CeleryConfig(object):
	CELERY_IMPORTS = ('')
	CELERY_TASK_RESULT_EXPIRES = 30
	CELERY_TIMEZONE = 'UTC'

	CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
	CELERY_TASK_SERIALIZER = 'json'
	CELERY_RESULT_SERIALIZER = 'json'

	CELERYBEAT_SCHEDULE = {
		'push-message': {
			'task': 'benedict.tasks.push_message_task.push_message',
			'schedule': crontab(minute="*")
		}
	}

class CeleryTestConfig(CeleryConfig):
	pass

class CeleryProductionConfig(CeleryConfig):
	pass