import time

import utils.intents_utils
from utils import config_utils


def what_time_is_it():
    current_time = time.localtime()
    response = utils.intents_utils.get_response("what_time_is_it")

    if config_utils.get_in_config("12HOURS-FORMAT"):
        response = response.replace('{time}', time.strftime("%I:%M %p", current_time))
    else:
        response = response.replace('{time}', time.strftime("%H:%M", current_time))

    return response


def what_day_is_it():
    return ""
