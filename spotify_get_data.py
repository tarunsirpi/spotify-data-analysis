import pandas as pd
import numpy as np

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

keys = pd.read_csv('spotify-keys.csv')

# keys['Client ID'][0]

cid = keys['Client ID'][0]
secret = keys['Client secret'][0]
# scope = 'user-follow-read'
# redirect_uri = 'http://localhost:8888/callback'

# from spotipy.oauth2 import SpotifyOAuth

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager= client_credentials_manager)


arr_id = '1mYsTxnqsietFxj1OgoGbG'
arr = sp.artist(arr_id)

album_ids = []
albums_required = 100

for i in range(0,albums_required,50):
    albums = sp.artist_albums(arr_id, limit = 50, offset=i)
    for item in albums['items']:
        album_id = item['id']
        album_ids.append(album_id)
        print(album_id)

# test_id = album_ids[10]
# tracks = sp.album_tracks(test_id, limit = 50)

# temp = []

tracks_df = pd.DataFrame(columns=['track_id', 'track_name', 'album_id'])

track_ids = []

for album_id in album_ids:

    tracks = sp.album_tracks(album_id, limit = 50)
    for track in tracks['items']:
        artists_list = []
        for artist in track['artists']:
            artists_list.append(artist['id'])
        if arr_id not in artists_list:
            continue

        track_name= track['name']
        track_id = track['id']
        print(track_name, track_id)
        if track_id in track_ids:
            continue
        track_ids.append(track_id)
        tracks_df.loc[len(tracks_df)] = [track_id, track_name, album_id]



album_df = pd.DataFrame(columns=['album_id', 'album_name', 'release_date', 'release_date_precision', 'total_tracks', 'album_type'])

for album_id in album_ids:
    album = sp.album(album_id)

    album_name = album['name']
    release_date = album['release_date']
    release_date_precision = album['release_date_precision']
    total_tracks = album['total_tracks']
    album_type = album['album_type']

    album_df.loc[len(album_df)] = [album_id, album_name, release_date, release_date_precision, total_tracks, album_type]


tracks_list = list(tracks_df['track_id'])

track_audio_features_df = pd.DataFrame(columns = ['track_id', 'popularity', 'danceability', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature'])

for track_id in tracks_list:

    track = sp.track(track_id)
    popularity = track['popularity']

    audio_features = sp.audio_features(track_id)[0]

    danceability= audio_features['danceability']
    key= audio_features['key']
    loudness= audio_features['loudness']
    mode= audio_features['mode']
    speechiness= audio_features['speechiness']
    acousticness= audio_features['acousticness']
    instrumentalness= audio_features['instrumentalness']
    liveness= audio_features['liveness']
    valence= audio_features['valence']
    tempo= audio_features['tempo']
    duration_ms= audio_features['duration_ms']
    time_signature= audio_features['time_signature']

    track_audio_features_df.loc[len(track_audio_features_df)] = [track_id, popularity, danceability, key, loudness, mode, speechiness, acousticness,
                                                                 instrumentalness, liveness, valence, tempo, duration_ms, time_signature]


track_audio_features_df.to_csv('data/track_audio_features_df.csv', index=False)

tracks_df.to_csv('data/tracks_df.csv', index=False)

album_df.to_csv('data/album_df.csv', index=False)
