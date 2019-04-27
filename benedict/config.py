import os


def get_db_url(env):
    if env == "Development":
        return os.environ.get("SQLALCHEMY_DATABASE_URI") or "postgresql:///benedict"
    else:
        return os.environ['DATABASE_URL']
