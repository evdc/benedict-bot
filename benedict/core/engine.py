import json
import logging

from celery import Celery
from celery.schedules import schedule
from redbeat.schedulers import RedBeatSchedulerEntry

from benedict.interfaces.dynamodb_client import DynamoDBBackend

log = logging.getLogger(__name__)

celery = Celery(__name__)
celery.config_from_object('benedict.config.celeryconfig')

class Engine(object):
	"""Handles application management. 
	will delegate to brain for response logic etc."""
	def __init__(self):
		self.db = DynamoDBBackend()
		self.schedule_entry = None

	def handle_message(self, message):
		log.info("Received message: ", message)
		self.db.save_message(message)

		if message['text'].lower() == "start":
			e = RedBeatSchedulerEntry('push-message',
									  	'benedict.tasks.push_message_task.push_message',
									  	schedule(run_every=10),
									  	args=('184544168823830', 'Hello from Benedict!'), 
									  	app=celery
									 )
			e.save()
			self.schedule_entry = e 	# TODO - have this be a map of some kind?
			return "Starting."

		if message['text'].lower() == "stop":
			e = RedBeatSchedulerEntry.from_key(self.schedule_entry.key, app=celery)
			e.delete()
			self.schedule_entry = None
			return "Stopping."	

		return "Hello from Benedict!"

	def start_schedule(self):
		pass

	def stop_schedule(self):
		pass
