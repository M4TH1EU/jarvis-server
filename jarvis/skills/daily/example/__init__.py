from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler


class ExampleSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("ExampleSkill", data)

    @intent_file_handler("example_intent.intent", "ExampleIntent")
    def handle_example_intent(self, data):
        pass


def create_skill(data):
    return ExampleSkill(data)
