# test_fbmessenger.py

import pytest
import os
import tempfile

from benedict.server import create_server

@pytest.fixture
def client():
	app = create_server(env='Test')
	db_fd, app.config['DATABASE'] = tempfile.mkstemp()
	app.testing = True
	client = app.test_client()
	yield client
	os.close(db_fd)
	os.unlink(app.config['DATABASE'])

def test_server(client):
	response = client.get("/fbmsg")
	assert response
	



