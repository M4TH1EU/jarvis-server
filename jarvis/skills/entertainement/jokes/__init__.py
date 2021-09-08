from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler
from jarvis.skills.entertainement.jokes.providers import jokes_french_provider, jokes_english_provider
from jarvis.utils import languages_utils


class JokesSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("JokesSkill", data)

    @intent_file_handler("tell_a_joke.intent", "TellAJokeIntent")
    def handle_joke(self, data):
        self.speak(get_joke(False))


def get_joke(nsfw, lang=languages_utils.get_language()):
    """
    Returns a joke in the good language

    Args:
        lang: use language from config by default, you can specify a custom language here
        nsfw: should include nsfw jokes

    Returns:
        array
    """
    if lang.startswith("fr-"):
        return jokes_french_provider.get_joke(nsfw)
    elif lang.startswith("en-"):
        return jokes_english_provider.get_joke(nsfw)
    else:
        return ['Error', "I don't know any jokes in your language..."]


def create_skill(data):
    return JokesSkill(data)
