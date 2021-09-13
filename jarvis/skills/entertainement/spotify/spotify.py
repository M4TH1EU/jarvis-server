import random
import re
import string
from difflib import SequenceMatcher

import spotipy
from lingua_franca.parse import fuzzy_match
from spotipy import SpotifyOAuth

from jarvis.utils import config_utils

scope = "user-read-playback-state, user-modify-playback-state, user-read-currently-playing"

# TODO: Investigate the open_browser and automatic auth renewing without user interaction

sp = None


def get_spotify():
    global sp
    if sp is None:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                       client_id=config_utils.get_in_secret("SPOTIFY_CLIENT_ID"),
                                                       client_secret=config_utils.get_in_secret(
                                                           "SPOTIFY_CLIENT_SECRET"),
                                                       redirect_uri='http://localhost:8888/callback/',
                                                       open_browser=False))
    return sp


def query_song(song=None, artist=None):
    if song is not None and artist is not None:
        query = '*{}* artist:{}'.format(song, artist)
    elif song is None and artist is not None:
        query = "artist:" + artist
    elif song is not None and artist is None:
        query = song
    else:
        song = "Back In Black AC/DC"  # proof that jarvis has a heart :)
        query = song

    data = get_spotify().search(q=query, limit=6, type='track')['tracks']['items']
    if data and len(data) > 0:
        if song is not None:
            tracks = [(best_confidence(d['name'], song), d) for d in data]
        else:
            tracks = [(best_confidence(d['name'], 'None'), d) for d in data]

        tracks.sort(key=lambda x: x[0])
        tracks.reverse()  # Place best matches first

        # Find pretty similar tracks to the best match
        # tracks = [t for t in tracks if t[0] > tracks[0][0] - 0.1]
        # Sort remaining tracks by popularity
        # tracks.sort(key=lambda x: x[1]['popularity'])

        return random.choice(tracks)[1]


def is_music_playing():
    return get_spotify().current_user_playing_track()['is_playing']


def best_confidence(title, query):
    """
    Find best match for a title against a query.
    Some titles include ( Remastered 2016 ) and similar info. This method
    will test the raw title and a version that has been parsed to remove
    such information.
    Arguments:
        title: title name from spotify search
        query: query from user
    Returns:
        (float) best condidence

    Thanks to @Mycroft source code for this code
    """
    if query == 'None':
        return SequenceMatcher(None, random_string_generator(5), random_string_generator(5)).ratio()

    best = title.lower()
    best_stripped = re.sub(r'(\(.+\)|-.+)$', '', best).strip()
    return max(fuzzy_match(best, query), fuzzy_match(best_stripped, query))


def random_string_generator(str_size):
    return ''.join(random.choice(string.ascii_letters + string.punctuation) for x in range(str_size))
