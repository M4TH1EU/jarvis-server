import speedtest

from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler


class SpeedTestSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("SpeedTestSkill", data)

    @intent_file_handler("start_speedtest.intent", "StartSpeedTestIntent")
    def handle_speedtest(self, data):
        try:
            self.speak_dialog_threaded('starting_speedtest')
            result = start_speedtest()

            down_speed = result[0]
            up_speed = result[1]
            self.speak_dialog('result_speedtest', {'DOWN': down_speed, 'UP': up_speed})
        except:
            self.speak("Error speedtest")


def start_speedtest():
    speed = speedtest.Speedtest(timeout=2)
    speed.get_servers([])
    speed.get_best_server()
    speed.download()
    speed.upload(pre_allocate=False)
    result = speed.results.dict()
    down_speed = ('%.2f' % float((result["download"]) / 1000000))
    up_speed = ('%.2f' % float((result["upload"]) / 1000000))

    return [down_speed, up_speed]


def create_skill(data):
    return SpeedTestSkill(data)
