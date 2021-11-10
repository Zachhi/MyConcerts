from django.shortcuts import render
import requests
from landing.credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging

def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print(
            "   %d %32.32s %s" %
            (i, track['artists'][0]['name'], track['name']))

def SpotifyAuth():
    SCOPE = "user-library-read, user-top-read, user-follow-read, user-read-email, user-read-private, playlist-read-private"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri = 'http://google.com', scope=SCOPE))

    
    #logger = logging.getLogger(__name__)
    results = sp.current_user_top_artists(limit=20, time_range='long_term')
    #logging.error("hello")
    #print(results['items']['artist'])
    #print('hey')s

SpotifyAuth()