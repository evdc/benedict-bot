import json
import logging

from celery.schedules import schedule
from redbeat.schedulers import RedBeatSchedulerEntry

from benedict.interfaces.dynamodb_client import DynamoDBBackend
from benedict.core.celery_app import app as celery_app

log = logging.getLogger(__name__)


class Engine(object):
    """Handles application management.
    will delegate to brain for response logic etc."""

    def __init__(self):
        # self.db = DynamoDBBackend()
        self.schedule_entry = None

    def handle_message(self, message):
        log.info("Received message: {}".format(message))
        # self.db.save_message(message)

        if message['text'].lower() == "start":
            self.start_schedule()
            return "Starting."

        if message['text'].lower() == "stop":
            self.stop_schedule()
            return "Stopping."

        return "Hello from Benedict!"

    def start_schedule(self):
        log.info("Starting worker ...")
        e = RedBeatSchedulerEntry('push-message',
                                  'benedict.core.tasks.push_message',
                                  schedule(run_every=10),
                                  args=('184544168823830', 'Hello from the scheduler.'),
                                  app=celery_app
                                  )
        e.save()
        self.schedule_entry = e  # TODO - have this be a map of some kind?

    def stop_schedule(self):
        log.info("Stopping worker ...")
        e = RedBeatSchedulerEntry.from_key(self.schedule_entry.key, app=celery_app)
        e.delete()
        self.schedule_entry = None
        pass