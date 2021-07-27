import requests as requests

from utils import languages_utils, config_utils


def tell_me_a_joke():
    tag = 'tell_me_a_joke'
    # response = intents_utils.get_response(tag)

    # french jokes
    if languages_utils.get_language().startswith("fr-"):

        # please register on www.blagues-api.fr and set a token in your secret
        response = requests.get(
            'https://www.blagues-api.fr/api/random',
            headers={
                'Authorization': 'Bearer ' + config_utils.get_in_secret('JOKES_FRENCH_API_TOKEN')
            }
        )

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
