import json
import os

from jarvis import get_path_file
from jarvis.utils import config_utils

path = os.path.dirname(get_path_file.__file__)


def get_language():
    return config_utils.get_in_config("LANGUAGE")


def get_language_full_name(name=None):
    """
    Return for exemple french for fr-fr, english for en-en, etc (savec in languages.json in the config folder)

    Return english if the language isn't found in the languages.json file
    """
    config_json = json.load(open(path + "/config/languages.json", encoding='utf-8', mode='r'))

    if name is None:
        name = get_language()

    if name in config_json:
        return config_json.get(name)

    return 'english'


def get_spacy_model(language=None):
    spacy_model = json.load(open(path + "/config/spacy.json", encoding='utf-8', mode='r'))

    if language is None:
        language = get_language()

    if language in spacy_model:
        return spacy_model.get(language)

    return 'xx_ent_wiki_sm'  # multi-language model (for unsupported languages)