import speedtest

from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler


class SpeedTestSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("SpeedTestSkill", data)

    @intent_file_handler("start_speedtest.intent", "StartSpeedTestIntent")
    def handle_speedtest(self, data):
        try:
            self.speak_dialog('starting_speedtest')

            speed = speedtest.Speedtest()
            # speed.get_servers([])
            speed.get_best_server()
            speed.download()
            speed.upload(pre_allocate=False)
            # speed.results.share()
            result = speed.results.dict()
            down_speed = ('%.2f' % float((result["download"]) / 1000000))
            up_speed = ('%.2f' % float((result["upload"]) / 1000000))

            self.speak_dialog('result', {'DOWN': down_speed, 'UP': up_speed})
        except:
            self.speak_dialog("error")


def create_skill(data):
    return SpeedTestSkill(data)
