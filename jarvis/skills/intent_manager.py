from adapt.engine import DomainIntentDeterminationEngine
from adapt.intent import IntentBuilder

engine = DomainIntentDeterminationEngine()


def register_entity(value, type, domain):
    engine.register_entity(entity_value=value, entity_type=type, domain=domain)

    print("entity : " + value + " / " + type + " / " + domain)
    # print("Registred entity : \"" + entity + "\" for domain : " + domain)


def register_regex(regex, domain):
    engine.register_regex_entity(regex, domain)
    # print("Registred regex : \"" + regex + "\" for domain : " + domain)


def register_intent(intent, domain):
    if domain not in engine.domains:
        engine.register_domain(domain)

    # TODO: INVESTIGATE WHY IT WORKS WHEN DID MANUALLY BUT DOESN'T WHEN DID AUTOMATICALLY VIA THE INTENT
    # register_entity('cherche', "Wikipedia", domain='WikipediaSkill')
    # register_regex('.*(wiki|sur|au sujet de|wikipedia)(?! (sur|au sujet)) (?P<ArticleTitle>.+)',
    #                domain='WikipediaSkill')

    # engine.register_entity('cherche', "Wikipedia", domain='WikipediaSkill')
    # engine.register_regex_entity('.*(wiki|sur|au sujet de|wikipedia)(?! (sur|au sujet)) (?P<ArticleTitle>.+)',
    #                             domain='WikipediaSkill')

    # intent = IntentBuilder("WikipediaQueryIntent").require("Wikipedia").optionally('ArticleTitle').build()

    engine.register_intent_parser(intent, domain='WikipediaSkill')
    # print("Registred intent : " + domain)


def recognise(sentence):
    for intents in engine.determine_intent(sentence):
        print(intents)
