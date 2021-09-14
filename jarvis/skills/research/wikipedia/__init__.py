from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler
from jarvis.skills.research.wikipedia import wikipedia
from jarvis.utils.fallbacks.wolframalpha import wa_client


class WikipediaSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("WikipediaSkill", data)

    @intent_file_handler("search.wikipedia.intent", "WikipediaQueryIntent")
    def handle_wikipedia_query_intent(self, data):
        if 'query' in data:
            self.speak(wikipedia.page_summary(query=data['query']))
        else:
            wolfram_response = wa_client.ask(data['utterance'])
            if wolfram_response is not None:
                self.speak(wolfram_response)


def create_skill(data):
    return WikipediaSkill(data)
