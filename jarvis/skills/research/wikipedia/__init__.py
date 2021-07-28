from adapt.intent import IntentBuilder

from jarvis.skills import Skill


class WikipediaSkill(Skill):
    def __init__(self):
        super().__init__("WikipediaSkill", "research", "wikipedia")

    def register(self):
        super().register()

        wikipedia_query_intent = IntentBuilder("WikipediaQueryIntent")\
            .require("Wikipedia")\
            .require("ArticleTitle")
        super().register_intent(wikipedia_query_intent)
