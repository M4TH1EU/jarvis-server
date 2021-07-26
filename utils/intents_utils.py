import json
import os
import random

import intents.intents


def get_patterns(intent_tag):
    if exists(intent_tag):
        patterns = get_lang_for_intent(intent_tag).get(intent_tag).get('patterns')
        return patterns
    else:
        return {}


def get_responses(intent_tag):
    if exists(intent_tag):
        responses = get_lang_for_intent(intent_tag).get(intent_tag).get('responses')
        return responses
    else:
        return {}


def get_response(intent_tag):
    if exists(intent_tag):
        responses = get_responses(intent_tag)
        return random.choice(responses)


def get_lang_for_intent(intent_tag):
    language = "fr-fr"  # TODO: use config value

    # first we check the intent
    if exists(intent_tag):
        lang_path = str(intents.intents.get_all_intents().get(intent_tag))
        lang_path = lang_path + 'lang/' + language + '.json'

        if os.path.exists(lang_path):
            lang_file = open(lang_path)
            json_lang = json.load(lang_file)
            return json_lang
    else:
        return {}


def exists(intent_tag):
    if intent_tag in intents.intents.get_all_intents():
        return True
    else:
        return False
