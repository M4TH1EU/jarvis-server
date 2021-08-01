import glob
import os
import random
import threading
import types

from jarvis import get_path_file
from jarvis.skills import intent_manager
from jarvis.utils import languages_utils, client_utils


class Skill:
    def __init__(self, name, data):
        self.name = name

        self.client_ip = data['client_ip']
        self.client_port = data['client_port']

        path = self.__module__.split(".")
        self.category = path[2]
        self.skill_folder = path[3]

        self.path = os.path.dirname(get_path_file.__file__) + "/skills/" + self.category + "/" + self.skill_folder

    def speak(self, sentence):
        client_utils.speak(sentence, self.client_ip, self.client_port)

    def speak_dialog(self, dialog, data=None):
        if data is None:
            data = {}

        file = self.path + "/dialog/" + languages_utils.get_language() + "/" + dialog + ".dialog"
        if os.path.exists(file):
            with open(file, "r") as infile:
                random_line = random.choice(infile.readlines())

                for key, val in data.items():
                    if "{{" + key + "}}" in random_line:

                        # TODO: replace when found a better TTS engine for french
                        # as the french tts don't support float in sentence, convert it to an integer
                        if is_float(val):
                            # val = str(int(float(val)))  # convert a float to integer
                            val = str(val).split(".")[0] + " virgule " + str(val).split(".")[1]

                        random_line = random_line.replace("{{" + key + "}}", val)

                infile.close()

            self.speak(random_line)

        return "Error, dialog not found for : " + dialog

    def speak_dialog_threaded(self, dialog, data=None):
        thread = threading.Thread(target=self.speak_dialog, args=[dialog, data])
        thread.start()

    def register(self):
        self.register_entities()
        self.register_regex()
        print("[" + self.name + "] Registered entity/entities and regex(s)")

    def register_entities(self):
        path = self.path + "/vocab/" + languages_utils.get_language() + "/*.voc"

        files = glob.glob(path, recursive=True)
        for file in files:
            with open(file, "r") as infile:
                for line in infile.readlines():
                    filename = file.split("/")[-1].split(".voc")[0]

                    intent_manager.register_entity_adapt(line.replace('\n', ''), filename, self.name)

    def register_regex(self):
        path = self.path + "/regex/" + languages_utils.get_language() + "/*.rx"

        files = glob.glob(path, recursive=True)
        for file in files:
            with open(file, "r") as infile:
                for line in infile.readlines():
                    intent_manager.register_regex_adapt(line.replace('\n', ''), self.name)


def get_array_for_intent_file(filename, category, skill_folder):
    path = os.path.dirname(get_path_file.__file__) + "/skills/" + category + "/" + skill_folder
    path = path + "/vocab/" + languages_utils.get_language() + "/" + filename

    with open(file=path, mode="r") as infile:
        lines = []

        for line in infile.readlines():
            lines.append(line.replace('\n', ''))

        return lines


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class SkillRegistering(type):
    def __init__(cls, name, bases, attrs):
        for key, val in attrs.items():
            if type(val) is types.FunctionType and not str(val).__contains__("__"):
                intent_type = getattr(val, "_type", None)

                if intent_type is not None:
                    properties = getattr(val, "_data", None)

                    if properties is not None:
                        if intent_type == 'adapt':
                            intent = properties[0]
                            intent_name = intent.name

                            intent_manager.intents_handlers_adapt[f"{intent_name}"] = [getattr(cls, key), name, key,
                                                                                       attrs['__module__']]
                        elif intent_type == 'padatious':
                            intent_file = properties[0]
                            intent_name = properties[1]

                            intent_category = str(attrs['__module__']).split('.')[2]
                            skill_folder = str(attrs['__module__']).split('.')[3]

                            intent_manager.intents_handlers_padatious[f"{intent_name}"] = [key,
                                                                                           get_array_for_intent_file(
                                                                                               intent_file,
                                                                                               intent_category,
                                                                                               skill_folder),
                                                                                           attrs['__module__']]
