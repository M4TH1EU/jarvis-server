import utils.intents_utils


def what_time_is_it():
    response = utils.intents_utils.get_response("what_time_is_it")
    response.replace("{time}", "18:41")
    return response


def what_day_is_it():
    return ""
