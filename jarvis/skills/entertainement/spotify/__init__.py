from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler
from jarvis.skills.entertainement.spotify import spotify


class SpotifySkill(Skill, metaclass=SkillRegistering):
    def __init__(self):
        super().__init__("SpotifySkill")

    @intent_file_handler("play_a_song.intent", "PlaySongWithSpotifyIntent")
    def handle_play_a_song(self, data):
        if 'song' in data:
            song_lists_matching = spotify.query_song(data['song'])
            if 'singer' in data:
                song_lists_matching = spotify.query_song(data['song'], data['singer'])

            if song_lists_matching is not None and len(song_lists_matching) >= 1:
                print(song_lists_matching[0]['uri'] + " / " + song_lists_matching[0]['name'] + " / " +
                      song_lists_matching[0]['artists'][0]['name'])
