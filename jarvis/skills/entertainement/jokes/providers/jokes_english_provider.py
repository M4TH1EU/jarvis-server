import requests


def get_joke(nsfw=False):
    """
    Returns a joke in 2 parts

    Args:
        nsfw: include nsfw jokes?

    Returns: array
    """

    url = 'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart'

    if nsfw:
        url = "https://v2.jokeapi.dev/joke/Any?type=twopart"

    # please register on www.blagues-api.fr and set a token in your secrets file
    response = requests.get(url)

    data = response.json()
    joke = data['setup']
    answer = data['delivery']

    return [joke, answer]
