import requests as requests

from utils import config_utils


def tell_me_a_joke():
    tag = 'tell_me_a_joke'
    # response = intents_utils.get_response(tag)

    # french jokes
    if config_utils.get_in_config("LANGUAGE").startswith("fr-"):
        # the token used might be revoked at any time, please register on www.blagues-api.fr and replace it
        response = requests.get(
            'https://www.blagues-api.fr/api/random',
            headers={
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzA4OTcyNzQwOTQ5ODM1ODI2IiwibGltaXQiOjEwMCwia2V5IjoiYmZlUVBSb2xuY2FleHBHc2taRU90VkdKOGxhdWZsZVRSMFJadnR3QXV3c056djdpYlkiLCJjcmVhdGVkX2F0IjoiMjAyMS0wNS0yOVQxNDoyMjo0MCswMDowMCIsImlhdCI6MTYyMjI5ODE2MH0.6VxH_dTdJSddhHoYOtdQl0j9WC3lzXjUujUio5U09Jg'
            }
        )

        data = response.json()
        joke = data['joke']
        answer = data['answer']

        return joke + " /pause:2s/ " + answer

    # english jokes
    elif config_utils.get_in_config("LANGUAGE").startswith("en-"):
        response = requests.get('https://v2.jokeapi.dev/joke/Any?type=twopart')
        data = response.json()

        joke = data['setup']
        answer = data['delivery']

        return joke + " /pause:2s/ " + answer
    else:
        return "I don't know any jokes in your language..."
