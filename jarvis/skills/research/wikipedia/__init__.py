from adapt.intent import IntentBuilder

from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_handler


class WikipediaSkill(Skill, metaclass=SkillRegistering):
    def __init__(self):
        super().__init__("WikipediaSkill")

    @intent_handler(IntentBuilder("WikipediaQueryIntent").require("Wikipedia").require("ArticleTitle"))
    def handle_wikipedia_query_intent(self, data):
        print("Handle Wikipedia Query Intent Method")


def create_skill():
    return WikipediaSkill()
