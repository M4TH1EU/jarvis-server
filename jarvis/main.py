import lingua_franca

from jarvis.skills import intent_manager
from jarvis.skills.daily.timer import TimerSkill
from jarvis.skills.entertainement.decide import DecideSkill
from jarvis.skills.entertainement.jokes import JokesSkill
from jarvis.skills.entertainement.moviemaster import MovieMaster
from jarvis.skills.entertainement.spotify import SpotifySkill
from jarvis.skills.entertainement.weather import WeatherSkill
from jarvis.skills.productivity.homeassistant import HomeAssistantSkill
from jarvis.skills.productivity.speedtest import SpeedTestSkill
from jarvis.skills.research.wikipedia import WikipediaSkill
from jarvis.utils import languages_utils, flask_utils


def start():
    # Load lingua franca in the memory
    # Supported : English French German Hungarian Italian Portuguese Swedish
    lingua_franca.load_language(lang=languages_utils.get_language_only_country())

    # Register all skills
    WikipediaSkill().register()
    JokesSkill().register()
    SpotifySkill().register()
    SpeedTestSkill().register()
    DecideSkill().register()
    TimerSkill().register()
    WeatherSkill().register()
    HomeAssistantSkill().register()
    MovieMaster().register()

    # TODO: calculator skill
    # TODO: google/ddg help skill
    # TODO: unit converter skill

    # Load all skills
    intent_manager.load_all_skills()

    # Train Padatious models
    intent_manager.train_padatious()

    # Bunch of tests
    # intent_manager.recognise("cherche Elon Musk sur wikipédia")  # WORKING
    # intent_manager.recognise("raconte moi une blague")  # WORKING
    # intent_manager.recognise("joue le morceau crazy crazy nights de KISS sur spotify")  # WORKING
    # intent_manager.recognise("coupe la musique")  # WORKING
    # intent_manager.recognise("c'est quoi le nom de cette chanson ?") # WORKING

    # Start the flask server
    flask_utils.start_server()
