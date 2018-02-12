import pytest

from benedict.interfaces.dynamodb_client import DynamoDBBackend

@pytest.fixture()
def client():
	cli = DynamoDBBackend()
	return cli 

def test_save_message(client):
	client.save_message({'user': 'abcdef', 'text': "~~TEST~~"})
