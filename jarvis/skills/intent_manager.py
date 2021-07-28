from adapt.engine import DomainIntentDeterminationEngine

engine = DomainIntentDeterminationEngine()


def register_entity(entity_value, entity_type, domain):
    engine.register_entity(entity_value=entity_value, entity_type=entity_type, domain=domain)
    print("[Adapt]: Added entity with type " + entity_type + " for " + domain)


def register_regex(regex, domain):
    engine.register_regex_entity(regex, domain)
    print("[Adapt]: Added new regex for " + domain)


def register_intent(intent, domain):
    engine.register_intent_parser(intent, domain='WikipediaSkill')
    print("[Adapt]: Registered new intent for skill " + domain)


def recognise(sentence):
    for intents in engine.determine_intent(sentence):
        print(intents)
