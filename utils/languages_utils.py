import json
import os

import get_path_file
from utils import config_utils

path = os.path.dirname(get_path_file.__file__)


def get_language():
    return config_utils.get_in_config("LANGUAGE")


def get_language_full_name(name=None):
    """
    Return for exemple french for fr-fr, english for en-en, etc (savec in languages.json in the config folder)
    """
    config_json = json.load(open(path + "/config/languages.json", encoding='utf-8', mode='r'))

    if name is None:
        name = get_language()

    if name in config_json:
        return config_json.get(name)
