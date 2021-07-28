import json

from adapt.engine import DomainIntentDeterminationEngine

engine = DomainIntentDeterminationEngine()

intents_handlers = dict()


def register_entity(entity_value, entity_type, domain):
    engine.register_entity(entity_value=entity_value, entity_type=entity_type, domain=domain)
    # print("[Adapt]: Added entity with type " + entity_type + " for " + domain)


def register_regex(regex, domain):
    engine.register_regex_entity(regex, domain)
    # print("[Adapt]: Added new regex for " + domain)


def register_intent(intent, domain):
    engine.register_intent_parser(intent, domain='WikipediaSkill')
    print("[Adapt]: Registered new intent for skill " + domain)


def process_handlers():
    for handler in intents_handlers:
        function_handler = intents_handlers.get(handler)
        intent_builder = getattr(function_handler[0], "_register", [])[0]
        skill_name = function_handler[1]

        register_intent(intent_builder.build(), domain=skill_name)


def handle(intent_name):
    if intent_name in intents_handlers:
        method = intents_handlers.get(intent_name)[0]
        method(None, [])


def recognise(sentence):
    for intents in engine.determine_intent(sentence):
        json_response = json.loads(json.dumps(intents))

        handle(json_response['intent_type'])
