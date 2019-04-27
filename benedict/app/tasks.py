import os

from benedict.app.sms import send_message


def send_reminder(number, name, message):
    m = "Hey {}! Don't forget {}.".format(name, message)
    print("Pinging {} from PID {}".format(number, os.getpid()))
    send_message(m, number)
