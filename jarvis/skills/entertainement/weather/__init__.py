from jarvis.skills import SkillRegistering, Skill
from jarvis.skills.decorators import intent_file_handler


class WeatherSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("WeatherSkill", data)

    @intent_file_handler("handle_weather.intent", "HandleWeatherIntent")
    def handle_weather(self, data):
        pass


def create_skill(data):
    return WeatherSkill(data)
