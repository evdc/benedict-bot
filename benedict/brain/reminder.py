import os

from apscheduler.schedulers.background import BackgroundScheduler

from benedict.brain.tasks import send_reminder
from benedict.config import get_db_url


class Reminder:
    def __init__(self):
        print("init Reminder")
        self.scheduled_jobs = {}
        self.scheduler = BackgroundScheduler(job_defaults={'coalesce': True})
        self.scheduler.add_jobstore('sqlalchemy', url=get_db_url(os.environ.get("FLASK_ENV", "Development")))
        self.scheduler.start()

    def set_reminder(self, user, at, message):
        job_id = "reminder_{}_{}".format(at, message)
        job = self.scheduler.add_job(send_reminder, id=id, args=(user.phone_number, user.name, message))
        self.scheduled_jobs[job_id] = job

    def clear_reminder(self, at, message):
        job_id = "reminder_{}_{}".format(at, message)
        self.scheduler.remove_job(job_id)
