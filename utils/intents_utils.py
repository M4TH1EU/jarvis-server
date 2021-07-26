import glob
import json
import os
import random

import get_path_file

all_intents = dict()
path = os.path.dirname(get_path_file.__file__)


def register_all_intents():
    global all_intents

    result = {}

    files = glob.glob(path + "/intents/**/info.json", recursive=True)
    for f in files:
        with open(f, "rb") as infile:
            intent_info_json = json.load(infile)
            intents_in_info = intent_info_json['intents']
            intent_path = str(f).replace('info.json', '')

            for intent in intents_in_info:
                result[intent] = intent_path

    all_intents = result


def get_all_intents():
    if len(all_intents) >= 1:
        return all_intents
    else:
        register_all_intents()
        return get_all_intents()


def get_all_patterns():
    all_patterns = {}

    # need to run register first
    if not all_intents:
        print("Warning : No intent found at all, don't forget to register them!")
        return {}

    for intent in all_intents:
        all_patterns[intent] = get_patterns(intent)

    return all_patterns


def get_patterns(intent_tag):
    if exists(intent_tag):
        patterns = get_lang_for_intent(intent_tag).get(intent_tag).get('patterns')
        return patterns
    else:
        return {}


def get_path(intent_tag):
    if exists(intent_tag):
        return get_all_intents().get(intent_tag)


def get_response(intent_tag):
    if exists(intent_tag):
        responses = get_responses(intent_tag)
        return random.choice(responses)


def get_responses(intent_tag):
    if exists(intent_tag):
        responses = get_lang_for_intent(intent_tag).get(intent_tag).get('responses')
        return responses
    else:
        return {}


def get_lang_for_intent(intent_tag):
    language = "fr-fr"  # TODO: use config value

    # first we check the intent
    if exists(intent_tag):
        lang_path = str(get_all_intents().get(intent_tag))
        lang_path = lang_path + 'lang/' + language + '.json'

        if os.path.exists(lang_path):
            lang_file = open(lang_path)
            json_lang = json.load(lang_file)
            return json_lang
    else:
        return {}


def exists(intent_tag):
    if intent_tag in get_all_intents():
        return True
    else:
        return False
