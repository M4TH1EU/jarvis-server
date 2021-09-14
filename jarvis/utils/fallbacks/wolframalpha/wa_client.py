import urllib.parse

import requests

from jarvis.utils import config_utils


def ask(sentence):
    query = urllib.parse.quote_plus(sentence)
    query_url = f"https://api.wolframalpha.com/v2/query?" \
                f"appid={config_utils.get_in_secret('WOLFRAM_APP_ID')}" \
                f"&input={query}" \
                f"&format=plaintext" \
                f"&output=json"

    r = requests.get(query_url).json()

    if r['queryresult']['success']:
        data = r["queryresult"]["pods"][1]["subpods"][0]
        return data['plaintext']
    else:
        return None
