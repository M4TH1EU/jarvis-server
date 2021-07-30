from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler
from jarvis.skills.research.wikipedia import wikipedia


class WikipediaSkill(Skill, metaclass=SkillRegistering):
    def __init__(self):
        super().__init__("WikipediaSkill")

    @intent_file_handler("search.wikipedia.intent", "WikipediaQueryIntent")
    def handle_wikipedia_query_intent(self, data):
        if 'query' in data:
            # TODO : say somethink like "i'm searching..."
            print("[INTENT RESULT] : " + wikipedia.page_summary(query=data['query']))
        else:
            # TODO: fallback to duckduckgo or wolfram alpha
            pass


def create_skill():
    return WikipediaSkill()
