import os

class Config(object):
	DEBUG = False
	TESTING = False

class TestConfig(Config):
	DEBUG = True
	TESTING = True

class ProductionConfig(Config):
	pass