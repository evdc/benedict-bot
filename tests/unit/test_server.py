# test_fbmessenger.py

import pytest
import json
import os
import tempfile

from benedict.service import create_app

@pytest.fixture
def client():
	app = create_app(env='Test')
	db_fd, app.config['DATABASE'] = tempfile.mkstemp()
	app.testing = True
	client = app.test_client()
	yield client
	os.close(db_fd)
	os.unlink(app.config['DATABASE'])

def test_fbmsg(client):
	response = client.get("/fbmsg")
	assert response.status_code == 200
	assert response.get_data(as_text=True) == "Hello World"

def test_fbmsg_verify(client):
	response = client.get("/fbmsg?hub.mode=subscribe&hub.challenge=foo&hub.verify_token=Q1W2E3R4T5")
	assert response.status_code == 200
	assert response.get_data(as_text=True) == "foo"

def test_fbmsg_post(client):
	data = {
		'object': 'page', 
		'entry': [{
			'messaging': [{
				'sender': {'id': '1845441168823830'}, 
				'recipient': {'id': '128995024567079'}, 
				'timestamp': 1517958975798, 
				'message': {
					'mid': 'mid.$cAAB1UabM_Axnnq0ZNlhbWe3KMXCq', 
					'seq': 327922, 
					'text': '~~TEST~~'}
			}], 
			'time': 1517983946393, 
			'id': '128995024567079'
		}]
	}
	response = client.post("/fbmsg", data=json.dumps(data), content_type="application/json")
	assert response.status_code == 200
	assert json.loads(response.get_data(as_text=True)) == {'response': 'Hello from Benedict!'}




