from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler
from jarvis.skills.entertainement.spotify import spotify


class SpotifySkill(Skill, metaclass=SkillRegistering):
    def __init__(self):
        super().__init__("SpotifySkill")

    @intent_file_handler("play_a_song.intent", "PlaySongWithSpotifyIntent")
    def handle_play_a_song(self, data):
        print(data)

        song_lists_matching = spotify.query_song(data['song'] if 'song' in data else None,
                                                 data['artist'] if 'artist' in data else None)

        if song_lists_matching is not None and len(song_lists_matching) >= 1:
            print(
                "[INFO INTENT] - Now playing : " + song_lists_matching[0]['uri'] + " / " + song_lists_matching[0][
                    'name'] + " / " +
                song_lists_matching[0]['artists'][0]['name'])

            spotify.get_spotify().add_to_queue(uri=song_lists_matching[0]['uri'])
            spotify.get_spotify().next_track()
            # spotify.get_spotify().start_playback(context_uri=song_lists_matching[0]['uri'])
        else:
            print("Nothing found for :" + str(data))

    @intent_file_handler("pause_music.intent", "PauseSpotifyIntent")
    def pause_music(self, data):
        spotify.get_spotify().pause_playback()
        print("[INFO INTENT] - Paused music for Spotify")

    @intent_file_handler("current_song.intent", "CurrentSongSpotifyIntent")
    def current_song(self, data):
        current_playback = spotify.get_spotify().current_playback()
        if current_playback['is_playing']:
            song_name = current_playback['item']['name']
            artist = current_playback['item']['artists'][0]['name']

            print("[INFO INTENT] - Current playback : " + song_name + " from " + artist + " on Spotify")
        else:
            print("Nothing is playing")


def create_skill():
    return SpotifySkill()
