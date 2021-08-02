from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler


class TimerSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("TimerSkill", data)

    @intent_file_handler("start_timer.intent", "StartTimerIntent")
    def handle_start_timer(self, data):
        print(data)
        pass


def create_skill(data):
    return TimerSkill(data)
