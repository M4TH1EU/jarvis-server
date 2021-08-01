import lingua_franca

from jarvis.skills import intent_manager
from jarvis.skills.entertainement.jokes import JokesSkill
from jarvis.skills.entertainement.spotify import SpotifySkill
from jarvis.skills.research.wikipedia import WikipediaSkill
from jarvis.utils import languages_utils, flask_utils, client_utils

if __name__ == '__main__':
    # Load lingua franca in the memory
    # Supported : English French German Hungarian Italian Portuguese Swedish
    lingua_franca.load_language(lang=languages_utils.get_language_only_country())

    # Tests
    WikipediaSkill().register()
    JokesSkill().register()
    SpotifySkill().register()

    # Load all skills
    intent_manager.load_all_skills()

    # Bunch of tests
    # intent_manager.recognise("cherche Elon Musk sur wikipédia")  # WORKING
    # intent_manager.recognise("raconte moi une blague")  # WORKING
    # intent_manager.recognise("joue le morceau crazy crazy nights de KISS sur spotify")  # WORKING
    # intent_manager.recognise("coupe la musique")  # WORKING
    # intent_manager.recognise("c'est quoi le nom de cette chanson ?") # WORKING

    # Start the flask server
    flask_utils.start_server()

