from flask import Flask, redirect, request, \
    Response, render_template
from flask.ext.heroku import Heroku
from twilio.twiml.messaging_response import MessagingResponse

from benedict.app.db import DB
from benedict.app.models import User
from benedict.app.models import Message as UserMessage
from benedict.app.sms import send_message
from benedict.app.utils import normalize_number

from benedict.brain.handler import get_response
from benedict.config import get_db_url


def create_app(env="Development"):
    app = Flask(__name__, static_url_path="/static")
    app.config["SQLALCHEMY_DATABASE_URI"] = get_db_url(env)

    heroku = Heroku(app)

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
    if user:
        message = body.lower()

        msg_object = UserMessage(
            user_id=user.id,
            raw=message
        )
        DB.session.add(msg_object)
        DB.session.commit()

        response = get_response(user, message)

        return response
    else:
        return "Please sign up and confirm first: https://benedict-bot.herokuapp.com"


if __name__ == "__main__":
    create_app()
