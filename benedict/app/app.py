import os

from flask import Flask, redirect, request, \
    Response, render_template
from twilio.twiml.messaging_response import MessagingResponse
from flask.ext.heroku import Heroku

from benedict.app.db import DB
from benedict.app.models import User
from benedict.app.models import Message as UserMessage
from benedict.app.sms import send_message
from benedict.app.utils import normalize_number


def create_app(env="Development"):
    app = Flask(__name__, static_url_path="/static")

    heroku = Heroku(app)

    if env == "Development":
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///benedict"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']

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
        # See: https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply-python
        # Webhook for the user texting us / twilio hits this
        print("Request values", request.values)
        body = request.values.get('Body', None)
        phone_number = request.values.get('From')
        phone_number = normalize_number(phone_number)

        resp = MessagingResponse()

        if body.lower() == 'confirm':
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
                resp.message("Thank you! Your path to happiness begins NOW!")
                return str(resp)
            else:
                return ''

        else:
            # check if user confirmed
            # if so do the regular response flow: store in db, thank the user
            user = DB.session.query(User).filter(
                User.phone_number == phone_number,
                User.confirmed == True
            ).one_or_none()
            print("found user: {}".format(user))
            if user:
                message = body.lower()

                msg_object = UserMessage(
                    user_id=user.id,
                    raw=body.lower(),
                    happiness=score
                )
                DB.session.add(msg_object)
                DB.session.commit()

                resp.message("Thanks for sharing. Your response has been recorded.".format(response_text))
            else:
                resp.message("Please sign up and confirm first.")
            return str(resp)

    DB.init_app(app)

    return app

if __name__ == "__main__":
    create_app()
