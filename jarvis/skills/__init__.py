import glob
import os
import random
import threading
import types

from .. import get_path_file
from ..skills import intent_manager
from ..utils import languages_utils, client_utils, config_utils


class Skill:
    def __init__(self, name, data, required_config: list = None):
        if required_config is not None:
            self.required_config = required_config

        self.name = name

        self.client_ip = data['client_ip']
        self.client_port = data['client_port']

        path = self.__module__.split(".")
        self.category = path[2]
        self.skill_folder = path[3]

        self.path = os.path.dirname(get_path_file.__file__) + "/skills/" + self.category + "/" + self.skill_folder

        if self.has_required_config():
            self.on_load()

    def on_load(self):
        pass

    def speak(self, sentence):
        client_utils.speak(sentence, self.client_ip, self.client_port)

    def speak_dialog(self, dialog, data=None):
        if data is None:
            data = {}

        file = self.path + "/dialog/" + languages_utils.get_language() + "/" + dialog + ".dialog"
        random_line = get_random_line_from_file(file)

        for key, val in data.items():
            if "{{" + key + "}}" in random_line or "{" + key + "}" in random_line:
                # TODO: replace when found a better TTS engine for french
                # as the french tts don't support float in sentence, convert it to an integer
                if is_float(val):
                    # val = str(int(float(val)))  # convert a float to integer
                    val = str(val).split(".")[0] + " virgule " + str(val).split(".")[1]

                random_line = random_line.replace("{{" + key + "}}", val)
                random_line = random_line.replace("{" + key + "}", val)

        self.speak(random_line)

        return "Error, dialog not found for : " + dialog

    def speak_dialog_threaded(self, dialog, data=None):
        thread = threading.Thread(target=self.speak_dialog, args=[dialog, data])
        thread.start()

    def register(self):
        if self.has_required_config():
            self.register_entities_adapt()
            self.register_entities_padatious()
            self.register_regex()
            print("[" + self.name + "] Registered entity/entities and regex(s)")
        else:
            print("[WARN] Skipped skill " + self.name + " : please check your config.")

    def register_entities_adapt(self):
        path = self.path + "/vocab/" + languages_utils.get_language() + "/*.voc"

        all_lines_by_file_dict = get_lines_of_all_files_in_path(path, return_as_dict_with_filename=True)

        for filename in all_lines_by_file_dict:
            for line in all_lines_by_file_dict.get(filename):
                intent_manager.register_entity_adapt(line, filename, self.name)

    def register_entities_padatious(self):
        path = self.path + "/vocab/" + languages_utils.get_language() + "/*.entity"

        all_lines_by_file_dict = get_lines_of_all_files_in_path(path, return_as_dict_with_filename=True)

        for filename in all_lines_by_file_dict:
            intent_manager.register_entity_padatious(filename, all_lines_by_file_dict.get(filename))

    def register_regex(self):
        path = self.path + "/regex/" + languages_utils.get_language() + "/*.rx"

        result = get_lines_of_all_files_in_path(path)
        for line in result:
            intent_manager.register_regex_adapt(line, self.name)

    def has_required_config(self):
        if hasattr(self, "required_config") and self.required_config is not None:
            for field in self.required_config:
                if config_utils.get_in_config(field) is None:
                    return False
        return True


def get_random_line_from_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as infile:
            random_line = random.choice(infile.readlines())
            infile.close()
            return random_line
    else:
        print("File " + filepath + " doesn't exist...")


def get_all_lines_from_file(filepath):
    if os.path.exists(filepath):
        with open(file=filepath, mode="r") as infile:
            lines = []

            for line in infile.readlines():
                lines.append(line.removesuffix('\n'))

            infile.close()

            return lines
    else:
        print("File " + filepath + " doesn't exist...")


def get_lines_of_all_files_in_path(path, return_as_dict_with_filename=False):
    files = glob.glob(path, recursive=True)
    result = dict()
    result_list = []

    for file in files:
        lines = get_all_lines_from_file(file)

        if return_as_dict_with_filename:
            filename = file.split("/")[-1].split('.')[0]
            result[filename] = lines
        else:
            result_list.extend(lines)

    if return_as_dict_with_filename:
        return result

    return result_list


def get_array_for_intent_file(filename, category, skill_folder):
    path = os.path.dirname(get_path_file.__file__) + "/skills/" + category + "/" + skill_folder
    path = path + "/vocab/" + languages_utils.get_language() + "/" + filename

    return get_all_lines_from_file(path)


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
