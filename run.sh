#!/bin/sh
celery worker -E -A benedict.core.celery_app &
celery beat -S redbeat.RedBeatScheduler -A benedict.core.celery_app &
gunicorn run:server -b 0.0.0.0:5000
