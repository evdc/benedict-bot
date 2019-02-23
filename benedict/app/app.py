import os
from datetime import datetime

from flask import Flask, redirect, request, \
    Response, render_template
from twilio.twiml.messaging_response import MessagingResponse
from flask.ext.heroku import Heroku

from benedict.app.db import DB
from benedict.app.models import User
from benedict.app.models import Message as UserMessage
from benedict.app.sms import send_message
from benedict.app.utils import normalize_number

from benedict.app.tasks import ping
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import ConflictingIdError

def get_db_url(env):
    if env == "Development":
        return os.environ.get("SQLALCHEMY_DATABASE_URI") or "postgresql:///benedict"
    else:
        return os.environ['DATABASE_URL']


def create_app(env="Development"):
    app = Flask(__name__, static_url_path="/static")
    app.config["SQLALCHEMY_DATABASE_URI"] = get_db_url(env)

    heroku = Heroku(app)

    print("Starting the scheduler in PID {}".format(os.getpid()))
    scheduler = BackgroundScheduler(job_defaults={'coalesce': True})
    scheduler.add_jobstore('sqlalchemy', url=app.config["SQLALCHEMY_DATABASE_URI"])
    scheduler.add_job(ping, 'interval', minutes=2, args=['18052848446'])
    scheduler.start()
    # try:
    #     scheduler.add_job(ping, 'interval', minutes=2, args=['18052848446'], id='ping')
    # except ConflictingIdError:
    #     pass

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/signup", methods=["POST"])
    def signup():
        phone_number = request.form['phone_number']
        print("Received signup for phone number {}".format(phone_number))
        send_message(body='Hello from Benedict! Please respond with CONFIRM to finish your registration.', to=phone_number)

        user = User(phone_number=phone_number)
        DB.session.add(user)
        DB.session.commit()

        return render_template('signed_up.html')

    @app.route("/message", methods=["GET", "POST"])
    def handle_response():
        print("Request values", request.values)
        body = request.values.get('Body', '')
        phone_number = request.values.get('From')
        phone_number = normalize_number(phone_number)

        resp = MessagingResponse()
        response_msg = ''
        if body.lower() == 'confirm':
            response_msg = handle_confirm(phone_number)
        else:
            response_msg = handle_regular_response(phone_number, body)
        resp.message(response_msg)
        return str(resp)

    DB.init_app(app)
    return app


def handle_confirm(phone_number):
    print("Looking for user with phone number {}".format(phone_number))
    user = DB.session.query(User).filter(
        User.phone_number == phone_number,
        User.confirmed == False
    ).one_or_none()
    print("query result: {}".format(user))

    if user:
        user.confirmed = True
        DB.session.add(user)
        DB.session.commit()
        return "Thanks! You're now confirmed."
    else:
        return "Please sign up first: https://benedict-bot.herokuapp.com"


def handle_regular_response(phone_number, body):
    user = DB.session.query(User).filter(
        User.phone_number == phone_number,
        User.confirmed == True
    ).one_or_none()
    print("found user: {}".format(user))
    if user:
        message = body.lower()

        msg_object = UserMessage(
            user_id=user.id,
            raw=body.lower()
        )
        DB.session.add(msg_object)
        DB.session.commit()

        return "Thanks for sharing. Your response has been recorded."
    else:
        return "Please sign up and confirm first: https://benedict-bot.herokuapp.com"


if __name__ == "__main__":
    create_app()
