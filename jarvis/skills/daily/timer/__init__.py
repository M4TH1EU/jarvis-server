from lingua_franca.parse import extract_duration

from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler
from jarvis.utils import languages_utils


class TimerSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("TimerSkill", data)

    def register(self):
        super(TimerSkill, self).register()


    @intent_file_handler("start_timer.intent", "StartTimerIntent")
    def handle_start_timer(self, data):
        print(data)
        if 'duration' in data:
            print(extract_duration(data['duration']), languages_utils.get_language())

            if 'name' in data:
                print("Start timer for {} named {}".format(data['duration'], data['name']))
                pass
            else:
                print("Start timer for {} without name".format(data['duration']))
                # TODO : ask for name
                pass
        else:
            print("No amount and/or time_unit")
        pass


def create_skill(data):
    return TimerSkill(data)
