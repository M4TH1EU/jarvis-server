import re

import spotipy
from lingua_franca.parse import fuzzy_match
from spotipy import SpotifyOAuth

from jarvis.utils import config_utils

scope = "user-read-playback-state, user-modify-playback-state, user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               client_id=config_utils.get_in_config("SPOTIFY_CLIENT_ID"),
                                               client_secret=config_utils.get_in_config("SPOTIFY_CLIENT_SECRET"),
                                               redirect_uri='http://localhost:8888/callback/',
                                               open_browser=False))
# TODO: Investigate the open_browser and automatic auth renewing without user interaction


def get_spotify():
    return sp


def query_song(song, artist=None):
    if song is not None and artist is not None:
        song_search = '*{}* artist:{}'.format(song, artist)
    else:
        song_search = song

    data = get_spotify().search(q=song_search, type='track')['tracks']['items']
    if data and len(data) > 0:
        tracks = [(best_confidence(d['name'], song), d)
                  for d in data]
        tracks.sort(key=lambda x: x[0])

        tracks.reverse()  # Place best matches first

        # Find pretty similar tracks to the best match
        tracks = [t for t in tracks if t[0] > tracks[0][0] - 0.1]

        # Sort remaining tracks by popularity
        tracks.sort(key=lambda x: x[1]['popularity'])
        # print([(t[0], t[1]['name'], t[1]['artists'][0]['name']) for t in tracks])  # DEBUG
        data = [tracks[-1][1]]

        # return tracks[-1][0], {'data': data, 'name': None, 'type': 'track'}
        return data


def best_confidence(title, query):
    """Find best match for a title against a query.
    Some titles include ( Remastered 2016 ) and similar info. This method
    will test the raw title and a version that has been parsed to remove
    such information.
    Arguments:
        title: title name from spotify search
        query: query from user
    Returns:
        (float) best condidence
    """
    best = title.lower()
    best_stripped = re.sub(r'(\(.+\)|-.+)$', '', best).strip()
    return max(fuzzy_match(best, query), fuzzy_match(best_stripped, query))
