import os
from benedict.app.app import create_app
from benedict.app.tasks import ping


env = os.environ.get("FLASK_ENV", "Development")
APP = create_app(env)

from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.add_jobstore('sqlalchemy', url=APP.config["SQLALCHEMY_DATABASE_URI"])
job = scheduler.add_job(ping, 'interval', minutes=2, args=['18052848446'])
scheduler.start()

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8080, APP)

    httpd.serve_forever()
