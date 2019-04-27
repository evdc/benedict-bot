import re

from benedict.brain.reminder import Reminder

reminder_regexp = re.compile(r'remind me (?P<action>\w+) at (?P<time>\d\d:\d\d)')

reminder = Reminder()


def get_response(user, message):
    # first limited version: "remind me to take out the trash at 17:00"
    reminder_match = reminder_regexp.match(message)
    if reminder_match:
        action, time = reminder_match.groups()
        print("Matched: ", reminder_match.groups())
        reminder.set_reminder(user, reminder_match.groupdict()["time"], reminder_match.groupdict()["action"])
        return "Ok, I'll remind you to {} at {}".format(action, time)
    else:
        return "Thanks!"

