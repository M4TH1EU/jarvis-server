import json

import flask
import speech_recognition as sr
from flask import Response, request, jsonify, Flask

from jarvis.skills import intent_manager
from jarvis.utils import config_utils, languages_utils

app = Flask(__name__)


@app.route("/process", methods=['POST'])
def process_request():
    data = get_data_in_request(request)

    if 'sentence' not in data or not data['sentence']:
        flask.abort(Response('You must provide a \'sentence\' parameter (not empty aswell)!'))

    return jsonify(intent_manager.recognise(sentence=data['sentence']))


@app.route("/process_audio_request", methods=['POST'])
def process_audio_request():
    frame_data = request.data
    sample_rate = 44100
    sample_width = 2

    r = sr.Recognizer()
    audio = sr.AudioData(frame_data, sample_rate, sample_width)

    result_stt = r.recognize_google(audio, language=languages_utils.get_language_only_country())

    return jsonify(intent_manager.recognise(sentence=result_stt))


def get_data_in_request(flask_request):
    data_str = str(flask_request.data.decode('utf8')).replace('"', '\"').replace("\'", "'")

    # if no data return an empty json to avoid error with json.loads below
    if not data_str:
        return {}

    data_json = json.loads(data_str)

    if not isinstance(data_json, dict):
        data_json = json.loads(data_json)

    return data_json


def start_server():
    app.config['JSON_AS_ASCII'] = False
    app.run(port=config_utils.get_in_config("PORT"), debug=False, host='0.0.0.0', threaded=True)
