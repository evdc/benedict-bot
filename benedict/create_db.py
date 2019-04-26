from benedict.app.db import DB
from benedict.app.app import create_app

if __name__ == "__main__":
    DB.app = create_app()
    DB.create_all()
