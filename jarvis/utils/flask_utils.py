import json
import tempfile

import flask
import speech_recognition as sr
from flask import Response, request, jsonify, Flask

from jarvis.skills import intent_manager
from jarvis.utils import config_utils, languages_utils

app = Flask(__name__)


@app.route("/process_text_request", methods=['POST'])
def process_text_request():
    data = get_data_in_request(request)

    if 'sentence' not in data or not data['sentence']:
        flask.abort(Response('You must provide a \'sentence\' parameter (not empty aswell)!'))

    return jsonify(intent_manager.recognise(data['sentence'], request.headers.get('Client-Ip'),
                                            request.headers.get('Client-Port')))


# RAW REQUEST
@app.route("/process_audio_request", methods=['POST'])
def process_audio_request():
    frame_data = request.data
    sample_rate = 44100
    sample_width = 2

    r = sr.Recognizer()
    audio = sr.AudioData(frame_data, sample_rate, sample_width)

    return recognition(r, audio)


# .WAV (i.e.) FILE REQUEST
@app.route("/process_audio_request_file", methods=['POST'])
def process_audio_request_android():
    temp = tempfile.NamedTemporaryFile(prefix='audio_', suffix='_android')
    temp.write(request.data)

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(temp.name) as source:
        audio = r.record(source)  # read the entire audio file

    temp.close()

    return recognition(r, audio)

def recognition(recognizer, audio):
    try:
        result_stt = recognizer.recognize_google(audio, language=languages_utils.get_language_only_country())

        return jsonify(
            intent_manager.recognise(result_stt, request.headers.get('Client-Ip'), request.headers.get('Client-Port')))

    except sr.UnknownValueError:
        error_msg = "[Error] No speech detected in the send audio!"
        print(error_msg)
        return jsonify(error_msg)


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
