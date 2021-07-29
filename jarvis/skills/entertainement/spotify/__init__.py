from adapt.intent import IntentBuilder

from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_handler


class SpotifySkill(Skill, metaclass=SkillRegistering):
    def __init__(self):
        super().__init__("SpotifySkill")

    @intent_handler(IntentBuilder("PlaySongOnlyTitle").require("Play").optionally("Spotify").optionally("SongNameOnly"))
    def handle_play_song_only_title(self, data):
        print("")

    @intent_handler(IntentBuilder("PlaySongTitleAndSinger").require("Play").optionally("Spotify").require("From").optionally("SongName").optionally("Singer"))
    def handle_play_song_title_and_singer(self, data):
        print("")