from fuzzywuzzy import fuzz
from homeassistant_api import Client

from jarvis.utils import config_utils

client = None


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


def find_entity(entity, types):
    """Find entity with specified name, fuzzy matching
    Throws request Exceptions
    (Subclasses of ConnectionError or RequestException,
      raises HTTPErrors if non-Ok status code)
    """
    json_data = client.get_states()
    # require a score above 50%
    best_score = 50
    best_entity = None
    if json_data:
        for state in json_data:
            try:
                if state['entity_id'].split(".")[0] in types:
                    # something like temperature outside
                    # should score on "outside temperature sensor"
                    # and repetitions should not count on my behalf
                    score = fuzz.token_sort_ratio(
                        entity,
                        state['attributes']['friendly_name'].lower())
                    if score > best_score:
                        best_score = score
                        best_entity = {
                            "id": state['entity_id'],
                            "dev_name": state['attributes']['friendly_name'],
                            "state": state['state'],
                            "best_score": best_score}
                    score = fuzz.token_sort_ratio(
                        entity,
                        state['entity_id'].lower())
                    if score > best_score:
                        best_score = score
                        best_entity = {
                            "id": state['entity_id'],
                            "dev_name": state['attributes']
                            ['friendly_name'],
                            "state": state['state'],
                            "best_score": best_score}
            except KeyError:
                pass
        return best_entity


def init():
    # init the client for the first time
    get_client()
