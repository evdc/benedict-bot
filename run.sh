#!/bin/sh
celery worker -A benedict.core.engine &
celery beat -S redbeat.RedBeatScheduler -A benedict.core.engine &
gunicorn run:server -b 0.0.0.0:5000
