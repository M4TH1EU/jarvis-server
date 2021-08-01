import requests
from requests.structures import CaseInsensitiveDict

from jarvis.utils import config_utils


def speak(sentence, client_ip, client_port):
    raw_audio_bytes = get_audio_from_sentence(sentence)
    if raw_audio_bytes is None:
        return "Error, audio not valid!"

    play_audio_on_client(raw_audio_bytes, client_ip, client_port)


def get_audio_from_sentence(sentence):
    voice = config_utils.get_in_config("TTS_VOICE")

    headers = {'accept': '*/*'}

    params = (
        ('voice', voice),
        ('text', sentence),
    )

    # TODO : add support for external opentts server
    try:
        response = requests.get('http://localhost:5500/api/tts', headers=headers, params=params)
        return response.content
    except requests.exceptions.ConnectionError:
        print("Error connecting to Open TTS server")
        return None


def play_audio_on_client(raw_audio_bytes, client_ip, client_port):
    url_service = "http://" + client_ip + ":" + client_port + "/play_raw_audio"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "text/xml; charset=utf8"

    response = requests.post(url_service,
                             headers=headers,
                             data=raw_audio_bytes)

    print(response.content)
