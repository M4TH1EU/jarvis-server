from adapt.engine import DomainIntentDeterminationEngine
from padatious import IntentContainer

adapt_engine = DomainIntentDeterminationEngine()
padatious_intents_container = IntentContainer('intent_cache')

intents_handlers_adapt = dict()
intents_handlers_padatious = dict()


def register_entity_adapt(entity_value, entity_type, domain):
    adapt_engine.register_entity(entity_value=entity_value, entity_type=entity_type, domain=domain)
    # print("[Adapt]: Added entity with type " + entity_type + " for " + domain)


def register_regex_adapt(regex, domain):
    adapt_engine.register_regex_entity(regex, domain)
    # print("[Adapt]: Added new regex for " + domain)


def register_intent_adapt(intent, domain):
    adapt_engine.register_intent_parser(intent, domain=domain)
    print("[Adapt]: Registered new intent " + intent.name + " for skill " + domain + ".")


def register_intent_padatious(intent_name, list_of_intent_examples):
    padatious_intents_container.add_intent(intent_name, list_of_intent_examples)
    print("[Padatious]: Registered new intent " + intent_name + " with " + str(
        len(list_of_intent_examples)) + " examples.")


def train_padatious():
    padatious_intents_container.train()


def process_handlers():
    for handler in intents_handlers_adapt:
        function_handler = intents_handlers_adapt.get(handler)
        intent_builder = getattr(function_handler[0], "_data", [])[0]
        skill_name = function_handler[1]
        register_intent_adapt(intent_builder.build(), domain=skill_name)

    for handler in intents_handlers_padatious:
        function_handler = intents_handlers_padatious.get(handler)
        intent_data_examples = function_handler[1]
        register_intent_padatious(handler, intent_data_examples)


def handle(intent_name, data):
    if intent_name in intents_handlers_adapt:
        method = intents_handlers_adapt.get(intent_name)[0]
        method(None, data)

    if intent_name in intents_handlers_padatious:
        method = intents_handlers_padatious.get(intent_name)[0]
        method(None, data)


def recognise(sentence):
    sentence = sentence.lower()
    print(sentence)

    if len(intents_handlers_adapt) > 0:
        try:
            best_intents = adapt_engine.determine_intent(sentence, 100)
            best_intent = next(best_intents)

            print(best_intent)  # DEBUG

            # TODO: add data for adapt
            handle(best_intent['intent_type'], [])
        except StopIteration as e:
            print("No match... (Adapt)")

    if len(intents_handlers_padatious) > 0:
        result = padatious_intents_container.calc_intent(sentence)
        # print(result)  # DEBUG
        # print(padatious_intents_container.calc_intents(sentence))  # DEBUG

        if result.conf >= 0.2:
            data = dict()
            if isinstance(result.sent, list):
                data['utterance'] = " ".join(
                    result.sent)  # add the sentence (utterance) to the data given to the intent handler
            else:
                data['utterance'] = result.sent
            data.update(result.matches)  # adding the matches from padatious to the data
            handle(result.name, data)
        else:
            print("No match... (Padatious)")
