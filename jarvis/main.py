import flask
import lingua_franca
from flask import Flask, request, jsonify, Response

from jarvis.skills import intent_manager
from jarvis.skills.entertainement.jokes import JokesSkill
from jarvis.skills.entertainement.spotify import SpotifySkill
from jarvis.skills.research.wikipedia import WikipediaSkill
from jarvis.utils import languages_utils
from utils import config_utils, flask_utils

app = Flask(__name__)


@app.route("/process", methods=['POST'])
def process_request():
    data = flask_utils.get_data_in_request(request)

    if 'sentence' not in data or not data['sentence']:
        flask.abort(Response('You must provide a \'sentence\' parameter (not empty aswell)!'))

    return jsonify(intent_manager.recognise(sentence=data['sentence']))


if __name__ == '__main__':
    # Load lingua franca in the memory
    # Supported : English French German Hungarian Italian Portuguese Swedish
    lingua_franca.load_language(lang=languages_utils.get_language_only_country())

    # Tests
    WikipediaSkill().register()
    JokesSkill().register()
    SpotifySkill().register()

    intent_manager.load_all_skills()

    # intent_manager.recognise("cherche Elon Musk sur wikipédia")  # TO CHECK
    # intent_manager.recognise("raconte moi une blague")  # WORKING
    # intent_manager.recognise("joue le morceau crazy crazy nights de KISS sur spotify")  # WORKING
    # intent_manager.recognise("coupe la musique")  # WORKING
    # intent_manager.recognise("c'est quoi le nom de cette chanson ?") # WORKING

    # start the flask server
    app.config['JSON_AS_ASCII'] = False
    app.run(port=config_utils.get_in_config("PORT"), debug=False, host='0.0.0.0', threaded=True)
