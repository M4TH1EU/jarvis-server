import requests

from jarvis.utils import config_utils


def get_joke(nsfw=False):
    """
    Returns a joke in 2 parts

    Args:
        nsfw: include nsfw jokes?

    Returns: array
    """

    url = 'https://www.blagues-api.fr/api/random'

    if nsfw:
        url = url + "?disallow=dark&disallow=limit"

    # please register on www.blagues-api.fr and set a token in your secrets file
    response = requests.get(url, headers={
        'Authorization': 'Bearer ' + config_utils.get_in_secret('JOKES_FRENCH_API_TOKEN')})

    data = response.json()
    joke = data['joke']
    answer = data['answer']

    return [joke, answer]
