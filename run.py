import os

from benedict.service import create_app, setup_celery


env = os.environ.get("FLASK_ENV", "Test")
server = create_app(env=env)

celery = setup_celery(server)

if __name__ == "__main__":
	server.run()