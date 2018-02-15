web: gunicorn run:server --log-file=-
worker: celery worker -A run
beat: celery beat -A run