import os

from benedict.service import create_app

env = os.environ.get("FLASK_ENV", "Test")
server = create_app(env=env)

if __name__ == "__main__":
    server.run()
