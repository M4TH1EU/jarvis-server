from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler


class WikipediaSkill(Skill, metaclass=SkillRegistering):
    def __init__(self):
        super().__init__("WikipediaSkill")

    @intent_file_handler("search.wikipedia.intent", "WikipediaQueryIntent")
    def handle_wikipedia_query_intent(self, data):
        print(data)
        print("Handle Wikipedia Query Intent Method")


def create_skill():
    return WikipediaSkill()
