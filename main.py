import flask
from flask import Flask, request, jsonify, Response

import ia.process
from utils import config_utils, flask_utils

app = Flask(__name__)


@app.route("/process", methods=['POST'])
def process_request():
    data = flask_utils.get_data_in_request(request)

    if 'sentence' not in data or not data['sentence']:
        flask.abort(Response('You must provide a \'sentence\' parameter (not empty aswell)!'))

    sentence = data['sentence']
    tag_for_request = ia.process.get_tag_for_sentence(sentence)

    print("SENTENCE : " + sentence + " /// TAG : " + tag_for_request)

    return jsonify(tag_for_request)


if __name__ == '__main__':
    # start the flask server
    app.config['JSON_AS_ASCII'] = False
    app.run(port=config_utils.get_in_config("PORT"), debug=False, host='0.0.0.0', threaded=True)