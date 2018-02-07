import json
import logging

class Engine(object):
	"""Handles application management. will delegate to brain for response logic etc."""
	def __init__(self):
		pass

	def handle_message(self, message):
		return "Hello from Benedict!"		
