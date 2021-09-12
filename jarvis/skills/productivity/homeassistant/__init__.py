from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler
from jarvis.skills.productivity.homeassistant import homeassistant_client


class HomeAssistantSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("HomeAssistantSkill", data)
        homeassistant_client.init()

    @intent_file_handler("homeassistant_turn_on.intent", "HATurnOn")
    def handle_turn_on(self, data):
        print(homeassistant_client.find_switchable_entity(data['entity']))


def create_skill(data):
    return HomeAssistantSkill(data)
