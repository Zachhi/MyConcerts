from django.shortcuts import render, redirect
from django.urls import reverse
import requests
from landing.credentials import CLIENT_ID, CLIENT_SECRET, SCOPE
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import credentials
from datetime import date
import urllib

# Spotify API User Authentification - sp is an OAuth Object
sp = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri = 'http://127.0.0.1:8000/callback', scope=SCOPE)

def spotify_auth(request, has_spotify):
    # SCOPE = "user-library-read, user-top-read, user-follow-read, user-read-email, user-read-private, playlist-read-private"

    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE))

    # results = sp.current_user_top_artists(limit=20, time_range='long_term')
    # print(results['items']['artist'])
    if has_spotify == 'yes':
        auth_url = sp.get_authorize_url()
        return redirect(auth_url)
    else:
        return redirect('landing-home', page='1')
    #return render(request, 'landing/spotifyauth'

#provides a callback from spotify_auth. Also used to parse out token and to pass spotipy object to landing/home
def callback(request):
    url = request.build_absolute_uri()
    code = sp.parse_response_code(url)
    token = sp.get_access_token(code)
    token_info = sp.get_cached_token()

    request.session["token_ID"] = token_info["access_token"]
    print(request.session['token_ID'])
    request.session["token"] = token_info
    return redirect('landing-home', page='1')
    #return redirect('login')
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




def login_home(request):
    return render(request, "landing/loginhome.html")

def home(request, page): 

    userlisttop = get_spotify_info(request)
    top_artist = userlisttop["topartists"][0]
    print(top_artist)

    events = ticket_master_request(page=page)
    return render(request, "landing/home.html", {"events": events, "page": page, 'title':'Landing'})
    # events has elements name, url, image, date, time, venue, city, state, min_price, max_price

def ticket_master_request(genre = 'Country', city = '', page = 1, start_date = date.today().strftime("%Y-%m-%d"), end_date = '2022-12-25'):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json?&countryCode=US&apikey=HCme8Zo9DSUpVKCGGF9CbgcTKO3YbsjE&page=' + str(page)
    if(city != ''):
        url = url + '&city=' + city
    if(genre != ''):
        url = url + '&classificationName=' + genre
    if(start_date != ''):
        url = url + '&startDateTime=' + start_date + 'T00:00:00Z'
    if(end_date != ''):
        url = url + '&endDateTime=' + end_date + 'T00:00:00Z'

    print(url)
    response = requests.get(url) 

    concerts = response.json()
    try:
        concerts = concerts["_embedded"]
    except: 
        return("error")
    events_from_api = concerts["events"]


    events = list()

    for e in events_from_api:
        dictionary = {}

        dictionary["name"] = e["name"]
        dictionary["url"] = e["url"]
        dictionary["image"] = e["images"][0]["url"]
        try: 
            if e["dates"]["start"]["dateTBA"] == False:
                dictionary["date"] = e["dates"]["start"]["localDate"]
            else:
                dictionary["date"] = "TBA"
        except:
            dictionary["date"] = "TBA"
        
        try: 
            if(e["dates"]["start"]["timeTBA"] == False):
                dictionary["time"] = e["dates"]["start"]['localTime']
            else: 
                dictionary["time"] = "TBA"
        except:
            dictionary["time"] = "TBA"

        dictionary["venue"] = e["_embedded"]["venues"][0]["name"]
        dictionary["city"] = e["_embedded"]["venues"][0]["city"]["name"]
        dictionary["state"] = e["_embedded"]["venues"][0]["state"]["name"]
        
        try:
            dictionary["min_price"] = e["priceRanges"][0]["min"]
        except: 
            dictionary["min_price"] = "TBA"

        try:
            dictionary["max_price"] = e["priceRanges"][0]["max"]
        except: 
            dictionary["max_price"] = "TBA"

        # genres
        try:
            dictionary["genres"] = e["classifications"][0]["genre"]["name"]
        except:
            dictionary["genres"] = "Unknown"

        try:
            dictionary["subgenre"] = e["classifications"][0]["subgenre"]["name"]
        except:
            dictionary["subgenre"] = "Unknown"

        if(e["sales"]["public"]["startTBA"] == False or e["sales"]["public"]["startTBD"] == False ):
            dictionary["salesStart"] = e["sales"]["public"]["startDateTime"]
        else:
            dictionary["salesStart"] = "TBA"

        # sales
        # please note
        try:
            dictionary["note"] = e["pleaseNote"]
        except:
            dictionary["note"] = "Unknown"
       
        # address
        try:
            dictionary["address"] = e["_embedded"]["venues"][0]["address"]["line1"]
        except:
            dictionary["address"] = "Unknown"
       

        # box office info
        try:
            dictionary["boxPhone"] = e["_embedded"]["venues"][0]["boxOfficeInfo"]["phoneNumberDetail"]
        except:
            dictionary["boxPhone"] = "Unknown"
        
        try:
            dictionary["boxHours"] = e["_embedded"]["venues"][0]["boxOfficeInfo"]["openHoursDetail"]
        except:
            dictionary["boxHours"] = "Unknown"
        

        try:
            dictionary["boxPayment"] = e["_embedded"]["venues"][0]["boxOfficeInfo"]["acceptedPaymentDetail"]
        except:
            dictionary["boxPayment"] = "Unknown"

        try:
            dictionary["boxWillCall"] = e["_embedded"]["venues"][0]["boxOfficeInfo"]["willCallDetail"]
        except:
            dictionary["boxWillCall"] = "Unknown"

        # parking
        try:
            dictionary["parking"] = e["_embedded"]["venues"][0]["parkingDetail"]
        except:
            dictionary["parking"] = "Unknown"

        try:
            dictionary["seating"] = e["_embedded"]["venues"][0]["accessibleSeatingDetail"]
        except:
            dictionary["seating"] = "Unknown"
        # general info

        try:
            dictionary["generalRule"] = e["_embedded"]["venues"][0]["generalInfo"]["generalRule"]
        except:
            dictionary["generalRule"] = "Unknown"

        try:
            dictionary["childRule"] = e["_embedded"]["venues"][0]["generalInfo"]["childRule"]
        except:
            dictionary["childRule"] = "Unknown"
        
        #print(dictionary["address"])
        #print(dictionary["boxPhone"])
        #print(dictionary["boxHours"])
        #print(dictionary["boxPayment"])
        #print(dictionary["boxWillCall"])
        #print(dictionary["parking"])
        #print(dictionary["seating"])
        #print(dictionary["generalRule"])
        #print(dictionary["childRule"])

        # social media links
        try:
            dictionary["instagram"] = e["_embedded"]["attractions"][0]["externalLinks"]["instagram"]
        except:
            dictionary["instagram"] = "Unknown"

        try:
            dictionary["twitter"] = e["_embedded"]["attractions"][0]["externalLinks"]["twitter"]
        except:
            dictionary["twitter"] = "Unknown"

        try:
            dictionary["facebook"] = e["_embedded"]["attractions"][0]["externalLinks"]["facebook"]
        except:
            dictionary["facebook"] = "Unknown"

        try:
            dictionary["youtube"] = e["_embedded"]["attractions"][0]["externalLinks"]["youtube"]
        except:
            dictionary["youtube"] = "Unknown"
        
        try:
            dictionary["homepage"] = e["_embedded"]["attractions"][0]["externalLinks"]["homepage"]
        except:
            dictionary["homepage"] = "Unknown"

        events.append(dictionary)

    return events

def about(request):
    return render(request, 'landing/about.html', {'title':'About'}) 

def detail(request):
    event = {}
    event["name"] = request.GET.get("name")
    event["image"] = request.GET.get("image")
    event["city"] = request.GET.get("city")
    print(event["city"])
    event["state"] = request.GET.get("state")
    event["min_price"] = request.GET.get("min_price")
    event["max_price"] = request.GET.get("max_price")
    event["url"] = request.GET.get("url")
    #event = urllib.parse.urlparse(data)
    #print("event:", event)
    return render(request, "landing/detail.html", {"event": event})


