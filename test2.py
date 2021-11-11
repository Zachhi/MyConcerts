# Shows a user's playlists (need to be authenticated via oauth)
from landing.credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import spotipy
from spotipy.oauth2 import SpotifyOAuth


import spotipy
from spotipy.oauth2 import SpotifyOAuth


def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print(
            "   %d %32.32s %s" %
            (i, track['artists'][0]['name'], track['name']))


if __name__ == '__main__':
    scope = 'playlist-read-private'
    SCOPE = "user-library-read, user-top-read, user-follow-read, user-read-email, user-read-private, playlist-read-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri = 'https://www.google.com', show_dialog = False, scope=SCOPE))

    playlists = sp.current_user_playlists()
    user_id = sp.me()['id']

    for playlist in playlists['items']:
        if playlist['owner']['id'] == user_id:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])

            results = sp.playlist(playlist['id'], fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks)

            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)