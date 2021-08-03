"""
Based on the Open-Source Mycroft Weather Skill
https://github.com/MycroftAI/skill-weather/blob/21.02/skill/weather.py
"""

from adapt.intent import IntentBuilder

from ... import Skill, SkillRegistering
from ...decorators import intent_handler, intent_file_handler


class WeatherSkill(Skill, metaclass=SkillRegistering):
    """Main skill code for the weather skill."""

    def __init__(self, data=dict):
        super().__init__("WeatherSkill", data)


    @intent_handler(
        IntentBuilder("handle_number_days_forecast")
            .optionally("query")
            .one_of("weather", "forecast")
            .require("number-days")
            .optionally("location")
    )
    # pas ouf
    def handle_number_days_forecast(self, data):
        """Handle multiple day forecast without specified location.

        Examples:
            "What is the 3 day forecast?"
            "What is the weather forecast?"

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_one_day_forecast")
            .optionally("query")
            .one_of("weather", "forecast")
            .require("relative-day")
            .optionally("location")
    )
    def handle_one_day_forecast(self, data):
        """Handle forecast for a single day.

        Examples:
            "What is the weather forecast tomorrow?"
            "What is the weather forecast on Tuesday in Baltimore?"

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_weather_later")
            .require("query")
            .require("weather")
            .require("later")
            .optionally("location")
    )
    def handle_weather_later(self, data):
        """Handle future weather requests such as: what's the weather later?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_weather_at_time")
            .optionally("query")
            .one_of("weather", "forecast")
            .require("relative-time")
            .optionally("relative-day")
            .optionally("location")
    )
    def handle_weather_at_time(self, data):
        """Handle future weather requests such as: what's the weather tonight?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_weekend_forecast")
            .require("query")
            .one_of("weather", "forecast")
            .require("weekend")
            .optionally("location")
    )
    def handle_weekend_forecast(self, data):
        """Handle requests for the weekend forecast.

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_week_weather")
            .optionally("query")
            .one_of("weather", "forecast")
            .require("week")
            .optionally("location")
    )
    def handle_week_weather(self, data):
        """Handle weather for week (i.e. seven days).

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_current_temperature")
            .optionally("query")
            .require("temperature")
            .optionally("location")
            .optionally("unit")
            .optionally("today")
            .optionally("now")
    )
    def handle_current_temperature(self, data):
        """Handle requests for current temperature.

        Examples:
            "What is the temperature in Celsius?"
            "What is the temperature in Baltimore now?"

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_daily_temperature")
            .optionally("query")
            .require("temperature")
            .require("relative-day")
            .optionally("location")
            .optionally("unit")
    )
    def handle_daily_temperature(self, data):
        """Handle simple requests for current temperature.

        Examples: "What is the temperature?"

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_hourly_temperature")
            .optionally("query")
            .require("temperature")
            .require("relative-time")
            .optionally("relative-day")
            .optionally("location")
    )
    def handle_hourly_temperature(self, data):
        """Handle requests for current temperature at a relative time.

        Examples:
            "What is the temperature tonight?"
            "What is the temperature tomorrow morning?"

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_high_temperature")
            .optionally("query")
            .require("high")
            .optionally("temperature")
            .optionally("location")
            .optionally("unit")
            .optionally("relative-day")
            .optionally("now")
            .optionally("today")
    )
    def handle_high_temperature(self, data):
        """Handle a request for the high temperature.

        Examples:
            "What is the high temperature tomorrow?"
            "What is the high temperature in London on Tuesday?"

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_low_temperature")
            .optionally("query")
            .require("low")
            .optionally("temperature")
            .optionally("location")
            .optionally("unit")
            .optionally("relative-day")
            .optionally("now")
            .optionally("today")
    )
    def handle_low_temperature(self, data):
        """Handle a request for the high temperature.

        Examples:
            "What is the high temperature tomorrow?"
            "What is the high temperature in London on Tuesday?"

        Args:
            data Bus event information from the intent parser
        """

        pass

    @intent_handler(
        IntentBuilder("handle_is_it_hot")
            .require("confirm-query-current")
            .one_of("hot", "cold")
            .optionally("location")
            .optionally("today")
    )
    def handle_is_it_hot(self, data):
        """Handler for temperature requests such as: is it going to be hot today?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_how_hot_or_cold")
            .optionally("query")
            .one_of("hot", "cold")
            .require("confirm-query")
            .optionally("location")
            .optionally("relative-day")
            .optionally("today")
    )
    def handle_how_hot_or_cold(self, data):
        """Handler for temperature requests such as: how cold will it be today?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_is_it_windy")
            .require("confirm-query")
            .require("windy")
            .optionally("location")
            .optionally("relative-day")
    )
    def handle_is_it_windy(self, data):
        """Handler for weather requests such as: is it windy today?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_windy")
            .require("how")
            .require("windy")
            .optionally("confirm-query")
            .optionally("relative-day")
            .optionally("location")
    )
    def handle_windy(self, data):
        """Handler for weather requests such as: how windy is it?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_is_it_snowing")
            .require("confirm-query")
            .require("snow")
            .optionally("location")
    )
    def handle_is_it_snowing(self, data):
        """Handler for weather requests such as: is it snowing today?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_is_it_clear")
            .require("confirm-query")
            .require("clear")
            .optionally("location")
    )
    def handle_is_it_clear(self, data):
        """Handler for weather requests such as: is the sky clear today?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_is_it_cloudy")
            .require("confirm-query")
            .require("clouds")
            .optionally("location")
            .optionally("relative-time")
    )
    def handle_is_it_cloudy(self, data):
        """Handler for weather requests such as: is it cloudy today?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_is_it_foggy").require("ConfirmQuery").require("Fog").optionally("Location")
    )
    def handle_is_it_foggy(self, data):
        """Handler for weather requests such as: is it foggy today?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_is_it_raining").require("ConfirmQuery").require("Rain").optionally("Location")
    )
    def handle_is_it_raining(self, data):
        """Handler for weather requests such as: is it raining today?

        Args:
            data Bus event information from the intent parser
        """
        pass

    # @intent_file_handler("do-i-need-an-umbrella.intent", "handle_need_umbrella")
    def handle_need_umbrella(self, data):
        """Handler for weather requests such as: will I need an umbrella today?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_is_it_storming")
            .require("ConfirmQuery")
            .require("Thunderstorm")
            .optionally("Location")
    )
    def handle_is_it_storming(self, data):
        """Handler for weather requests such as:  is it storming today?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_next_precipitation")
            .require("When")
            .optionally("Next")
            .require("Precipitation")
            .optionally("Location")
    )
    def handle_next_precipitation(self, data):
        """Handler for weather requests such as: when will it rain next?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_humidity")
            .require("Query")
            .require("Humidity")
            .optionally("RelativeDay")
            .optionally("Location")
    )
    def handle_humidity(self, data):
        """Handler for weather requests such as: how humid is it?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_sunrise")
            .one_of("Query", "When")
            .optionally("Location")
            .require("Sunrise")
            .optionally("Today")
            .optionally("RelativeDay")
    )
    def handle_sunrise(self, data):
        """Handler for weather requests such as: when is the sunrise?

        Args:
            data Bus event information from the intent parser
        """
        pass

    @intent_handler(
        IntentBuilder("handle_sunset")
            .one_of("Query", "When")
            .require("Sunset")
            .optionally("Location")
            .optionally("Today")
            .optionally("RelativeDay")
    )
    def handle_sunset(self, data):
        """Handler for weather requests such as: when is the sunset?

        Args:
            data Bus event information from the intent parser
        """
        pass


def create_skill(data):
    """Boilerplate to invoke the weather skill."""
    return WeatherSkill(data)
