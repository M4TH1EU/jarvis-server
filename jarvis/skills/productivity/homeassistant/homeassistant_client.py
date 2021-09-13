import glob
import itertools
import json
import os

from fuzzywuzzy import fuzz
from homeassistant_api import Client
from homeassistant_api.errors import ParameterMissingError

from jarvis import get_path_file
from jarvis.utils import config_utils

client = None
overridden_entities = dict()


def get_entites_from_type(type: str):
    return get_client().get_entities().__getattr__(type).entities


def find_switchable_entity(entity):
    ha_entity = find_entity(
        entity,
        [
            'group',
            'light',
            'fan',
            'switch',
            'scene',
            'input_boolean',
            'climate'
        ]
    )

    return ha_entity


def get_client():
    global client
    if client is None:
        client = Client(config_utils.get_in_secret('HOMEASSISTANT_API_URL') + "/api/",
                        config_utils.get_in_secret('HOMEASSISTANT_API_TOKEN'))

    return client


def find_entity(name, types):
    """Find entity with specified name, fuzzy matching
    Throws request Exceptions
    (Subclasses of ConnectionError or RequestException,
      raises HTTPErrors if non-Ok status code)
    """
    json_data = get_client().get_states()
    # require a score above 50%
    best_score = 50
    best_entity = None

    # Check if the friendly name is overriden manually (from the config files)
    if is_overridden(name):
        try:
            actionable_entity = get_client().get_entity(entity_id=get_entity_with_overridden_name(name))

            result = {
                "id": actionable_entity.entity_id,
                "dev_name": actionable_entity.state['attributes']['friendly_name'],
                "state": actionable_entity.state['state'],
                "best_score": 101}
            return result
        except ParameterMissingError:
            print("[Error] : Entity with id : " + get_entity_with_overridden_name(name) + " doesn't exists.")
            return None

    elif json_data:
        for state in json_data:
            try:
                if state['entity_id'].split(".")[0] in types:
                    # something like temperature outside
                    # should score on "outside temperature sensor"
                    # and repetitions should not count on my behalf
                    score = fuzz.token_sort_ratio(
                        name,
                        state['attributes']['friendly_name'].lower())
                    if score > best_score:
                        best_score = score
                        best_entity = {
                            "id": state['entity_id'],
                            "dev_name": state['attributes']['friendly_name'],
                            "state": state['state'],
                            "best_score": best_score
                        }

                    score = fuzz.token_sort_ratio(
                        name,
                        state['entity_id'].lower())
                    if score > best_score:
                        best_score = score
                        best_entity = {
                            "id": state['entity_id'],
                            "dev_name": state['attributes']['friendly_name'],
                            "state": state['state'],
                            "best_score": best_score
                        }
            except KeyError:
                pass
        return best_entity


def register_overrides():
    global overridden_entities
    files = glob.glob(os.path.dirname(get_path_file.__file__) + "/config/homeassistant/override/*.json")

    for file in files:
        file_json = json.load(open(file, encoding="utf8"))
        friendly_names = file_json['friendly_names']
        entity = file_json['entity']

        overridden_entities[entity] = friendly_names

    if len(overridden_entities) >= 1:
        print("[HomeAssistantSkill] Override for entities : " + str(list(overridden_entities.keys())))


def is_overridden(entity_friendly_name):
    values = list(itertools.chain.from_iterable(overridden_entities.values()))
    if entity_friendly_name in values:
        return True

    return False


def get_entity_with_overridden_name(friendly_name):
    scores = dict()
    for key, value in overridden_entities.items():
        for val in value:
            score = fuzz.token_sort_ratio(friendly_name, val)
            if score > 50:
                scores[score] = key

    if len(scores) >= 1:
        return sorted(scores.items(), reverse=True)[0][1]

    return None


def init():
    # init the client for the first time
    get_client()

    # register all the overrides entity from the config/homeassistant/override/ folder
    if not overridden_entities:
        register_overrides()
