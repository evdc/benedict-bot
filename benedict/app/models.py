from datetime import datetime

from sqlalchemy.orm import validates

from benedict.app.db import DB
from benedict.app.utils import normalize_number


class User(DB.Model):
    __tablename__ = "users"

    id = DB.Column(DB.Integer, primary_key=True)
    phone_number = DB.Column(DB.Text, nullable=False, unique=True)
    confirmed = DB.Column(DB.Boolean, nullable=False, default=False)
    last_active = DB.Column(DB.DateTime)

    @validates("phone_number")
    def validate_phone_number(self, _, phone_number):
        return normalize_number(phone_number)


class Message(DB.Model):
    __tablename__ = "Messages"

    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    timestamp = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)
    raw = DB.Column(DB.Text, nullable=False)
