FROM python:3.6-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_ENV Production

EXPOSE 5000
RUN celery worker -A benedict.core.engine
RUN celery beat -S redbeat.RedBeatScheduler -A benedict.core.engine
CMD gunicorn run:server -b 0.0.0.0:5000