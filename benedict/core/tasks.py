import logging
from celery.utils.log import get_task_logger

from benedict.core.celery_app import app
from benedict.interfaces.fbmessenger import send_message

log = get_task_logger(__name__)
logging.basicConfig(level=logging.INFO)


@app.task(bind=True)
def push_message(self, user_id, message_text):
    # TODO - future - call a reference to the Engine here?
    log.info("SENDING MESSAGE {} TO {}".format(message_text, user_id))
    send_message(user_id, message_text)