import os
from celery.schedules import crontab

CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
BROKER_URL = CELERY_BROKER_URL
REDBEAT_REDIS_URL = CELERY_BROKER_URL
redbeat_redis_url = CELERY_BROKER_URL

CELERY_IMPORTS = ('benedict.tasks.push_message_task')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULER = 'redbeat.RedBeatScheduler'
CELERYBEAT_MAX_LOOP_INTERVAL = 5