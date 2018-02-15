import celery

from benedict.interfaces.fbmessenger import send_message


@celery.task()
def push_message():
	# TODO - future - call a reference to the Engine here?
	# send_message(user_id, message_text)
	print("Hello, World~~")