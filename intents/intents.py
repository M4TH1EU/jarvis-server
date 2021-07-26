import glob
import json
import os

import get_path_file

intents = dict()
path = os.path.dirname(get_path_file.__file__)


def register_all_intents():
    global intents

    result = {}

    files = glob.glob(path + "/intents/**/info.json", recursive=True)
    for f in files:
        with open(f, "rb") as infile:
            intent_info_json = json.load(infile)
            intents_in_info = intent_info_json['intents']
            intent_path = str(f).replace('info.json', '')

            for intent in intents_in_info:
                result[intent] = intent_path

    intents = result


def get_all_intents():
    if len(intents) >= 1:
        return intents
    else:
        register_all_intents()
        return get_all_intents()


if __name__ == '__main__':
    print(get_all_intents())
