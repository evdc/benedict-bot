import os
from celery.schedules import crontab

CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

CELERY_IMPORTS = ('benedict.tasks.push_message_task')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# TODO - we will want this to be more dynamic
CELERYBEAT_SCHEDULE = {
	'push-message': {
		'task': 'benedict.tasks.push_message_task.push_message',
		'schedule': crontab(minute="*"),
		'kwargs': {
			'user_id': '1845441168823830',
			'message_text': 'Hello from Benedict!'
		}
	}
}