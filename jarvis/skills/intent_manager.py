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
    engine.register_intent_parser(intent, domain=domain)
    print("[Adapt]: Registered new intent " + intent.name + " for skill " + domain)


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
    sentence = sentence.lower()
    print(sentence)

    best_intents = engine.determine_intent(sentence, 100)
    best_intent = next(best_intents)

    print(best_intent)

    handle(best_intent['intent_type'])
