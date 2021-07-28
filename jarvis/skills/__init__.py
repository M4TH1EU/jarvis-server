import glob
import os

from jarvis import get_path_file
from jarvis.skills import intent_manager
from jarvis.utils import languages_utils


class Skill:
    def __init__(self, name, category, skill_folder):
        self.name = name
        self.category = category
        self.skill_folder = skill_folder

    def register(self):
        self.register_entities()
        self.register_regex()
        print("[" + self.name + "] Registered entity/entities and regex(s)")

    def register_entities(self):
        path = os.path.dirname(get_path_file.__file__) + "/skills/" + self.category + "/" + self.skill_folder
        path = path + "/vocab/" + languages_utils.get_language() + "/*.voc"

        files = glob.glob(path, recursive=True)
        for file in files:
            with open(file, "r") as infile:
                for line in infile.readlines():
                    filename = file.split("/")[-1].split(".voc")[0]

                    intent_manager.register_entity(line.replace('\n', ''), filename, self.name)

    def register_regex(self):
        path = os.path.dirname(get_path_file.__file__) + "/skills/" + self.category + "/" + self.skill_folder
        path = path + "/regex/" + languages_utils.get_language() + "/*.rx"

        files = glob.glob(path, recursive=True)
        for file in files:
            with open(file, "r") as infile:
                for line in infile.readlines():
                    intent_manager.register_regex(line.replace('\n', ''), self.name)

    def register_intent(self, intent):
        intent_manager.register_intent(intent.build(), domain=self.name)
