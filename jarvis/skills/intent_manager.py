import json

from adapt.engine import DomainIntentDeterminationEngine
from padatious import IntentContainer

from jarvis.utils import utils

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


def load_all_skills():
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
    module_path_str = None
    handler_method_name = None

    if intent_name in intents_handlers_adapt:
        # something like handler_play_song_spotify (used to call the handler method from the skill imported below)
        handler_method_name = intents_handlers_adapt.get(intent_name)[2]

        # something like jarvis.skill.entertainment.spotify (used to import the create_skill method to create a new object)
        module_path_str = intents_handlers_adapt.get(intent_name)[3]
    if intent_name in intents_handlers_padatious:
        # something like handler_play_song_spotify (used to call the handler method from the skill imported below)
        handler_method_name = intents_handlers_padatious.get(intent_name)[0]

        # something like jarvis.skill.entertainment.spotify (used to import the create_skill method to create a new object)
        module_path_str = intents_handlers_padatious.get(intent_name)[2]

    if module_path_str is not None and handler_method_name is not None:
        # import the create_skill method from the skill using the skill module path
        create_skill_method = utils.import_method_from_string(module_path_str, "create_skill")

        data = {'client_ip': data['client_ip'], 'client_port': data['client_port']}

        # create a new object of the right skill for the utterance
        skill = create_skill_method(data)

        # import and call the handler method from the skill
        getattr(skill, handler_method_name)(data=data)


def recognise(sentence, client_ip=None, client_port=None):
    sentence = sentence.lower()
    print(sentence)

    if len(intents_handlers_adapt) > 0:
        try:
            best_intents = adapt_engine.determine_intent(sentence, 100)
            best_intent = next(best_intents)

            # print(best_intent)  # DEBUG

            handle(best_intent['intent_type'],
                   data={'utterance': sentence, 'client-ip': client_ip, 'client-port': client_port})

            return best_intent

        except StopIteration as e:
            pass
            # print("No match... (Adapt)")

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

            data['client_ip'] = client_ip
            data['client_port'] = client_port

            data.update(result.matches)  # adding the matches from padatious to the data
            handle(result.name, data)

            return json.dumps(str(result))

        else:
            pass
            # print("No match... (Padatious)")
    print()
