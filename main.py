import flask
from flask import Flask, request, jsonify, Response

import ia.process
from utils import config_utils, flask_utils, intents_utils, utils

app = Flask(__name__)


@app.route("/process", methods=['POST'])
def process_request():
    data = flask_utils.get_data_in_request(request)

    if 'sentence' not in data or not data['sentence']:
        flask.abort(Response('You must provide a \'sentence\' parameter (not empty aswell)!'))

    sentence = data['sentence']
    tag_for_request = ia.process.get_tag_for_sentence(sentence)

    print("SENTENCE : " + sentence + " /// TAG : " + tag_for_request)

    # stop here if the sentence isn't understood
    if tag_for_request == 'dont_understand':
        return jsonify("I didn't get that.")

    path_of_intent = intents_utils.get_path(tag_for_request)
    path_of_intent = path_of_intent.split('/intents/')[1].replace('/', '.')
    path_of_intent = "intents." + path_of_intent + "intent"

    method = utils.import_method_from_string(path_of_intent, tag_for_request)
    return jsonify(method())


if __name__ == '__main__':
    # start the flask server
    app.config['JSON_AS_ASCII'] = False
    app.run(port=config_utils.get_in_config("PORT"), debug=False, host='0.0.0.0', threaded=True)
