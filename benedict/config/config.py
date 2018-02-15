import os


class Config(object):
	DEBUG = False
	TESTING = False
	CELERY_BROKER_URL = 'redis://localhost:6379/0'

class TestConfig(Config):
	DEBUG = True
	TESTING = True

class ProductionConfig(Config):
	pass