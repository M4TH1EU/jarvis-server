from jarvis.skills import SkillRegistering, Skill
from jarvis.skills.decorators import intent_file_handler


class WeatherSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("WeatherSkill", data)

    @intent_file_handler("handle_weather.intent", "HandleWeatherIntent")
    def handle_weather(self, data):
        pass

    @intent_file_handler("handle_temperature.intent", "HandleTemperatureIntent")
    def handle_temperature(self, data):
        pass

    @intent_file_handler("handle_is_it_hot.intent", "HandleIsItHotIntent")
    def handle_is_it_hot(self, data):
        pass

    @intent_file_handler("handle_is_it_cold.intent", "HandleIsItColdIntent")
    def handle_is_it_cold(self, data):
        pass

    @intent_file_handler("handle_is_it_windy.intent", "HandleIsItWindyIntent")
    def handle_windy(self, data):
        pass

    @intent_file_handler("handle_is_it_snowing.intent", "HandleIsItSnowingIntent")
    def handle_snowning(self, data):
        pass

    @intent_file_handler("handle_is_it_clear.intent", "HandleIsItClearIntent")
    def handle_is_it_clear(self, data):
        pass

    @intent_file_handler("handle_is_it_cloudy.intent", "HandleIsItCloudyIntent")
    def handle_is_it_cloudy(self, data):
        pass

    @intent_file_handler("handle_is_it_foggy.intent", "HandleIsItFoggyIntent")
    def handle_is_it_foggy(self, data):
        pass

    @intent_file_handler("handle_is_it_raining.intent", "HandleIsItRainingIntent")
    def handle_is_it_raining(self, data):
        pass

    @intent_file_handler("handle_do_i_need_an_umbrella.intent", "HandleNeedUmbrellaIntent")
    def handle_need_umbrella(self, data):
        pass

    @intent_file_handler("handle_is_it_storming.intent", "HandleIsItStormingIntent")
    def handle_need_storming(self, data):
        pass

    @intent_file_handler("handle_is_it_humid.intent", "HandleIsItHumidIntent")
    def handle_is_it_humid(self, data):
        pass

    @intent_file_handler("handle_when_raining.intent", "HandleWhenRainingIntent")
    def handle_when_raining(self, data):
        pass

    @intent_file_handler("handle_sunrise.intent", "HandleSunriseIntent")
    def handle_sunrise(self, data):
        pass

    @intent_file_handler("handle_sunset.intent", "HandleSunsetIntent")
    def handle_sunset(self, data):
        pass


def create_skill(data):
    return WeatherSkill(data)
