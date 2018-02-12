import json
import logging

from benedict.interfaces.dynamodb_client import DynamoDBBackend

log = logging.getLogger(__name__)

class Engine(object):
	"""Handles application management. will delegate to brain for response logic etc."""
	def __init__(self):
		self.db = DynamoDBBackend()

	def handle_message(self, message):
		log.info("Received message: ", message)
		self.db.save_message(message)
		return "Hello from Benedict!"
