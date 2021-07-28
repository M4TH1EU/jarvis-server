from adapt.intent import IntentBuilder

from jarvis.skills import Skill, intent_manager


class WikipediaSkill(Skill):
    def __init__(self):
        super().__init__("WikipediaSkill", "research", "wikipedia")

    def register(self):
        super().register()

        intent_manager.register_intent(IntentBuilder("WikipediaQueryIntent").require("Wikipedia").require("ArticleTitle").build(),
                                       domain=self.name)
