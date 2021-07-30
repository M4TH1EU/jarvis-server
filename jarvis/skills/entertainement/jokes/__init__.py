import requests
from adapt.intent import IntentBuilder

from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_handler
from jarvis.utils import languages_utils, config_utils


def speak_joke():
    # french jokes
    if languages_utils.get_language().startswith("fr-"):
        # please register on www.blagues-api.fr and set a token in your secret
        response = requests.get('https://www.blagues-api.fr/api/random', headers={
            'Authorization': 'Bearer ' + config_utils.get_in_secret('JOKES_FRENCH_API_TOKEN')})

        data = response.json()
        joke = data['joke']
        answer = data['answer']

        return joke + " /pause:2s/ " + answer

    # english jokes
    elif languages_utils.get_language().startswith("en-"):
        response = requests.get('https://v2.jokeapi.dev/joke/Any?type=twopart')
        data = response.json()

        joke = data['setup']
        answer = data['delivery']

        return joke + " /pause:2s/ " + answer
    else:
        return "I don't know any jokes in your language..."


class JokesSkill(Skill, metaclass=SkillRegistering):
    def __init__(self):
        super().__init__("JokesSkill")

    @intent_handler(IntentBuilder("JokingIntent").require("Joke"))
    def handle_joke(self, data):
        print(speak_joke())


def create_skill():
    return JokesSkill()
