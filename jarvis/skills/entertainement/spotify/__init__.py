from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler


class SpotifySkill(Skill, metaclass=SkillRegistering):
    def __init__(self):
        super().__init__("SpotifySkill")

    @intent_file_handler("play_a_song.intent")
    def handle_play_a_song(self, data):
        print("Play song")
