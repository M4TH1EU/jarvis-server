from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler
from jarvis.skills.productivity.homeassistant import homeassistant_client


class HomeAssistantSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("HomeAssistantSkill", data,
                         required_config=['HOMEASSISTANT_API_TOKEN', 'HOMEASSISTANT_API_URL'])

    def on_load(self):
        homeassistant_client.init()

    @intent_file_handler("homeassistant_restart.intent", "HARestart")
    def handle_restart_ha(self, data):
        # TODO: ask for confirmation
        homeassistant_client.restart_ha()

    @intent_file_handler("homeassistant_shutdown.intent", "HAShutdown")
    def handle_shutdown_ha(self, data):
        # TODO: ask for confirmation
        homeassistant_client.restart_ha()

    @intent_file_handler("homeassistant_turn_on.intent", "HATurnOn")
    def handle_turn_on(self, data):
        result = homeassistant_client.find_switchable_entity(data['entity'])
        homeassistant_client.turn_on_entity(result.get('id'))

    @intent_file_handler("homeassistant_turn_off.intent", "HATurnOff")
    def handle_turn_off(self, data):
        result = homeassistant_client.find_switchable_entity(data['entity'])
        homeassistant_client.turn_off_entity(result.get('id'))


def create_skill(data):
    return HomeAssistantSkill(data)
