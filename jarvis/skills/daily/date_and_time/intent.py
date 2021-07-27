import time
from datetime import datetime

from jarvis.utils import intents_utils, config_utils


def what_time_is_it():
    tag = 'what_time_is_it'
    response = intents_utils.get_response(tag)

    current_time = time.localtime()

    if config_utils.get_in_config("12HOURS-FORMAT"):
        response = response.replace('{time}', time.strftime("%I:%M %p", current_time))
    else:
        response = response.replace('{time}', time.strftime("%H:%M", current_time))

    return response


def what_day_is_it():
    tag = 'what_day_is_it'
    response = intents_utils.get_response(tag)

    day_number = datetime.today().weekday()
    lang_json = intents_utils.get_lang_for_intent('what_day_is_it')['others']['days_of_week']

    response = response.replace('{day}', lang_json[str(day_number)])

    return response
