import boto3 as bt
from datetime import datetime
from uuid import uuid1

from benedict.utils import totimestamp


class DynamoDBBackend(object):
	"""Responsible for storing user messages and other data in DynamoDB."""
	def __init__(self):
		self.resource = bt.resource('dynamodb', region_name='us-east-1')
		self.table - self.resource.Table('benedict_messages')

	def save_message(self, message):
		# message expected as dict with keys user, text
		item = {
			'uid': uuid1().hex,
			'user': message['user'],
			'text': message['text'],
			'timestamp': totimestamp(datetime.utcnow()) 
		}

		self.table.put_item(Item=item)