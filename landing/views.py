from django.shortcuts import render, redirect
from django.urls import reverse
import requests
from landing.credentials import CLIENT_ID, CLIENT_SECRET, SCOPE
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import credentials
from datetime import date

# Spotify API User Authentification - sp is an OAuth Object
sp = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri = 'http://127.0.0.1:8000/callback', scope=SCOPE)

def spotify_auth(request):
    # SCOPE = "user-library-read, user-top-read, user-follow-read, user-read-email, user-read-private, playlist-read-private"

    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE))

    # results = sp.current_user_top_artists(limit=20, time_range='long_term')
    # print(results['items']['artist'])
    auth_url = sp.get_authorize_url()
    return redirect(auth_url)
    #return render(request, 'landing/spotifyauth'

#provides a callback from spotify_auth. Also used to parse out token and to pass spotipy object to landing/home
def callback(request):
    url = request.build_absolute_uri()
    code = sp.parse_response_code(url)
    token = sp.get_access_token(code)
    token_info = sp.get_cached_token()

    request.session["token_ID"] = token_info["access_token"]
    request.session["token"] = token_info
    return redirect('landing-home')
    #render(request, 'landing-home', {'user':user})


def get_spotify_info(request): #carefull will call authetentification each time its called.. so we really woudl like to only call once
    user = spotipy.client.Spotify(auth=request.session['token_ID'])
    #user = spotipy.client.Spotify(sp)
    topartists = user.current_user_top_artists(limit=20, time_range='long_term')
    toptracks = user.current_user_top_tracks(limit=20, time_range='long_term')

    try:
        toptrack = toptracks['items'][0]['name'] #try catch block here in case the user does not have any data
    except: 
        print("User does not have any toptracks")
        return()
    
    try:
        topartist = topartists['items'][0]['genres']
    except: 
        print("User does not have any top artists")
        return()    

    user_top = {}
    toptracks_name = []
    topartists_name = []
    topgenres_name = []
    
    for i in range(20):
        toptracks_name.append(toptracks['items'][i]['name'])
    user_top["toptracks"] = toptracks_name
    
    for i in range(20):
        topartists_name.append(topartists['items'][i]['name'])
    user_top["topartists"] = topartists_name
    
    for i in range(20):
        topgenres_name.append(topartists['items'][i]['genres'])
    user_top["topgenres"] = topgenres_name
    return user_top
    

#userlisttop = get_spotify_info()

#get_spotify_info()


def home(request):
    #print(userlisttop["topartists"])
    # try changing p = 2!!!!!!!!!!!!! on line above
    # super easy pagination-type querying 
    userlisttop = get_spotify_info(request)
    top_artist = userlisttop["topartists"][0]
    print(top_artist)
    
    events = ticket_master_request()
    
    return render(request, "landing/home.html", {"events": events})
    # events has elements name, url, image, date, time, venue, city, state, min_price, max_price


def about(request):
    return render(request, 'landing/about.html', {'title':'About'}) 
    



def ticket_master_request(genre = 'Country', city = 'Austin', page = 1, start_date = date.today().strftime("%Y-%m-%d"), end_date = '2022-12-25'):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json?&countryCode=US&apikey=HCme8Zo9DSUpVKCGGF9CbgcTKO3YbsjE&page=' + str(page)
    if(city != ''):
        url = url + '&city=' + city
    if(genre != ''):
        url = url + '&classificationName=' + genre
    if(start_date != ''):
        url = url + '&startDateTime=' + start_date + 'T00:00:00Z'
    if(end_date != ''):
        url = url + '&endDateTime=' +  end_date + 'T00:00:00Z'

    response = requests.get(url) 

    concerts = response.json()
    concerts = concerts["_embedded"]
    events_from_api = concerts["events"]


    events = list()

    for e in events_from_api:
        dictionary = {}

        dictionary["name"] = e["name"]
        #print(e["name"])
        dictionary["url"] = e["url"]
        #print(e["url"])
        dictionary["image"] = e["images"][0]["url"]
        #print(e["images"][0]["url"])
        if(e["dates"]["start"]["dateTBA"] == False):
            dictionary["date"] = e["dates"]["start"]["localDate"]
        #   print(e["dates"]["start"]["localDate"])
        else:
            dictionary["date"] = "TBA"
    
        if(e["dates"]["start"]["timeTBA"] == False):
            dictionary["time"] = e["dates"]["start"]['localTime']
        #    print(e["dates"]["start"]['localTime'])
        else: 
            dictionary["time"] = "TBA"

        dictionary["venue"] = e["_embedded"]["venues"][0]["name"]
        #print(e["_embedded"]["venues"][0]["name"])
        dictionary["city"] = e["_embedded"]["venues"][0]["city"]["name"]
        #print(e["_embedded"]["venues"][0]["city"]["name"])
        dictionary["state"] = e["_embedded"]["venues"][0]["state"]["name"]
        #print(e["_embedded"]["venues"][0]["state"]["name"])
        
        try:
            dictionary["min_price"] = e["priceRanges"][0]["min"]
            #print(e["priceRanges"][0]["min"])
        except: 
            dictionary["min_price"] = "TBA"

        try:
            dictionary["max_price"] = e["priceRanges"][0]["max"]
            #print(e["priceRanges"][0]["max"])
        except: 
            dictionary["max_price"] = "TBA"

        events.append(dictionary)

    return events
    