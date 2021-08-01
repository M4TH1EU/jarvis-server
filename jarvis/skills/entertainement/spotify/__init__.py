from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler
from jarvis.skills.entertainement.spotify import spotify


class SpotifySkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("SpotifySkill", data)

    @intent_file_handler("play_a_song.intent", "PlaySongWithSpotifyIntent")
    def handle_play_a_song(self, data):
        print(data)

        song_lists_matching = spotify.query_song(data['song'] if 'song' in data else None,
                                                 data['artist'] if 'artist' in data else None)

        if song_lists_matching is not None and len(song_lists_matching) >= 1:
            # pause the music then speak dialog
            spotify.get_spotify().pause_playback()

            if 'artist' in data and 'song' not in data:
                self.speak_dialog("play_from_artist", {'artist': song_lists_matching[0]['artists'][0]['name']})
            else:
                self.speak_dialog("play_song_from_artist", {'song': song_lists_matching[0][
                    'name'], 'artist': song_lists_matching[0]['artists'][0]['name']})

            spotify.get_spotify().add_to_queue(uri=song_lists_matching[0]['uri'])
            spotify.get_spotify().next_track()
        else:
            self.speak_dialog("nothing_found")

    @intent_file_handler("pause_music.intent", "PauseSpotifyIntent")
    def pause_music(self, data):
        if spotify.is_music_playing():
            spotify.get_spotify().pause_playback()
            self.speak_dialog("pause_spotify")
        else:
            self.speak_dialog("nothing_playing")

    @intent_file_handler("resume_music.intent", "ResumeSpotifyIntent")
    def resume_music(self, data):
        if not spotify.is_music_playing():
            self.speak_dialog("resume_music")
            spotify.get_spotify().start_playback()
        else:
            self.speak_dialog("already_playing")

    @intent_file_handler("current_song.intent", "CurrentSongSpotifyIntent")
    def current_song(self, data):
        current_playback = spotify.get_spotify().current_playback()
        if current_playback['is_playing']:
            song_name = current_playback['item']['name']
            artist = current_playback['item']['artists'][0]['name']

            self.speak_dialog("current_playing_song_from_artist", {'song': song_name, 'artist': artist})
        else:
            self.speak_dialog('nothing_playing')


def create_skill(data):
    return SpotifySkill(data)
