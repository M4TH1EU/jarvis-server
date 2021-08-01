import random

from adapt.intent import IntentBuilder

from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_handler


class DecideSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("DecideSkill", data)

    @intent_handler(IntentBuilder("DecideIntent").require("choice1").require("choice2").optionally("OrKeyword"))
    # @intent_file_handler("decide.intent", "DecideIntent")
    def handle_decide(self, data):
        print("decide")

        print(data)

        if 'choice1' in data and 'choice2' in data:
            choice = bool(random.getrandbits(1))

            if choice:
                self.speak(data['choice1'])
            else:
                self.speak(data['choice2'])
        else:
            print("no all choice")


def create_skill(data):
    return DecideSkill(data)
