from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UsernameField
from django.shortcuts import render
import requests
from landing.credentials import CLIENT_ID, CLIENT_SECRET, SCOPE
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import credentials
from users.models import Spotify_Notification_Cred
from datetime import date
import datetime
import urllib

# Spotify API User Authentification - sp is an OAuth Object
sp = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri = 'http://127.0.0.1:8000/callback', scope=SCOPE)

def spotify_auth(request):
    # SCOPE = "user-library-read, user-top-read, user-follow-read, user-read-email, user-read-private, playlist-read-private"

    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE))

    # results = sp.current_user_top_artists(limit=20, time_range='long_term')
    has_spotify = str(Spotify_Notification_Cred.objects.get(username = request.user))
    has_spotify = has_spotify.split(',')

    #if 'yes' in str(has_spotify):
    if('yes' in has_spotify[0]):
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
    topartists = user.current_user_top_artists(limit=20, time_range='long_term')
    toptracks = user.current_user_top_tracks(limit=20, time_range='long_term')

    toptracks_artist = [] 
    topartists_name = []
    topgenres_name = []


    user_top = {}

    #print(toptracks['items'][0]['album']['artists'][0]['name']) # this gets the name of the top track's artist
    
    for i in range(len(toptracks['items'])):
        toptracks_artist.append(toptracks['items'][i]['album']['artists'][0]['name'])
    user_top["toptracks_artist"] = toptracks_artist
    

    for i in range(len(topartists['items'])):
        topartists_name.append(topartists['items'][i]['name'])
        topgenres_name.append(topartists['items'][i]['genres'])
    user_top["topartists"] = topartists_name
    user_top["topgenres"] = topgenres_name

    return user_top

#userlisttop = get_spotify_info()

#get_spotify_info()


#def updateEvents(request, page, genre, city, page1, start_date, end_date, search):
#    print("hello")
#    events = ticket_master_request(genre, city, page1, start_date, end_date, search)
#    return render(request, "landing/home.html", {"events": events, "page": page, 'title':'Landing'})

def login_home(request):
    return render(request, "landing/loginhome.html")

def home(request, page): 
    #print(request.ID)
    
    if str(request.user) != "AnonymousUser": #someone is logged in
        print("in here")
        print(request.user)
        has_spotify = Spotify_Notification_Cred.objects.get(username = request.user)
        if 'yes' in str(has_spotify):
            userlisttop = get_spotify_info(request)
            print(userlisttop)
    #top_tracks = userlisttop["toptracks"][0]
    #print(top_tracks)

    events = ticket_master_request('', '', 1, date.today().strftime("%Y-%m-%d"), '2022-12-25', 'op')
    return render(request, "landing/home.html", {"events": events, "page": page, 'title':'Landing'})
    # events has elements name, url, image, date, time, venue, city, state, min_price, max_price

def ticket_master_request(genre, city, page, start_date, end_date, search):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json?&countryCode=US&apikey=HCme8Zo9DSUpVKCGGF9CbgcTKO3YbsjE&size=15&page=' + str(page)
    if(city != ''):
        url = url + '&city=' + city
    if(genre != ''):
        url = url + '&classificationName=' + genre
    if(start_date != ''):
        url = url + '&startDateTime=' + start_date + 'T00:00:00Z'
    if(end_date != ''):
        url = url + '&endDateTime=' + end_date + 'T00:00:00Z'
    if(search != ''):
        url = url + '&keyword=' + search 

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
                api_date = e["dates"]["start"]["localDate"]
                formatted_date = datetime.datetime.strptime(api_date, '%Y-%m-%d').strftime('%B %d, %Y')
                dictionary["date"] = formatted_date
            else:
                dictionary["date"] = "TBA"
        except:
            dictionary["date"] = "TBA"
        
        try: 
            if(e["dates"]["start"]["timeTBA"] == False):
                api_time = e["dates"]["start"]['localTime']
                formatted_time = datetime.datetime.strptime(api_time, '%H:%M:%S').strftime('%I:%M%p')
                dictionary["time"] = formatted_time
                
            else: 
                dictionary["time"] = "TBA"
        except:
            dictionary["time"] = "TBA"

        dictionary["venue"] = e["_embedded"]["venues"][0]["name"]
        dictionary["city"] = e["_embedded"]["venues"][0]["city"]["name"]
        dictionary["state"] = e["_embedded"]["venues"][0]["state"]["name"]
        
        try:
            dictionary["min_price"] = int(e["priceRanges"][0]["min"])
        except: 
            dictionary["min_price"] = "TBA"

        try:
            dictionary["max_price"] = int(e["priceRanges"][0]["max"])
        except: 
            dictionary["max_price"] = "TBA"

        # genres
        try:
            dictionary["genres"] = e["classifications"][0]["genre"]["name"]
        except:
            dictionary["genres"] = "Unknown"

        try:
            dictionary["subgenre"] = e["classifications"][0]["subGenre"]["name"]
        except:
            dictionary["subgenre"] = "Unknown"

        try:
            if(e["sales"]["public"]["startTBA"] == False or e["sales"]["public"]["startTBD"] == False ):
                api_sales = e["sales"]["public"]["startDateTime"]
                formatted_sales = datetime.datetime.strptime(api_sales, '%Y-%m-%dT%H:%M:%SZ').strftime('%B %d, %Y, %I:%M%p')
                dictionary["salesStart"] = formatted_sales
            else:
                dictionary["salesStart"] = "TBA"
        except:
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
            dictionary["instagram"] = e["_embedded"]["attractions"][0]["externalLinks"]["instagram"][0]["url"]
        except:
            dictionary["instagram"] = "Unknown"

        try:
            dictionary["twitter"] = e["_embedded"]["attractions"][0]["externalLinks"]["twitter"][0]["url"]
        except:
            dictionary["twitter"] = "Unknown"

        try:
            dictionary["facebook"] = e["_embedded"]["attractions"][0]["externalLinks"]["facebook"][0]["url"]
        except:
            dictionary["facebook"] = "Unknown"

        try:
            dictionary["youtube"] = e["_embedded"]["attractions"][0]["externalLinks"]["youtube"][0]["url"]
        except:
            dictionary["youtube"] = "Unknown"
        
        try:
            dictionary["homepage"] = e["_embedded"]["attractions"][0]["externalLinks"]["homepage"][0]["url"]
        except:
            dictionary["homepage"] = "Unknown"

        # print(dictionary["instagram"])
        dictionary["starred"] = "true"
        print("DICTIONARY", dictionary["starred"])

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
    event["date"] = request.GET.get("date")
    event["time"] = request.GET.get("time")
    event["venue"] = request.GET.get("venue")
    event["genres"] = request.GET.get("genres")
    event["subgenre"] = request.GET.get("subgenre")
    event["salesStart"] = request.GET.get("salesStart")
    event["note"] = request.GET.get("note")
    event["address"] = request.GET.get("address")
    event["boxPhone"] = request.GET.get("boxPhone")
    event["boxHours"] = request.GET.get("boxHours")
    event["boxPayment"] = request.GET.get("boxPayment")
    event["boxWillCall"] = request.GET.get("boxWillCall")
    event["parking"] = request.GET.get("parking")
    event["seating"] = request.GET.get("seating")
    event["generalRule"] = request.GET.get("generalRule")
    event["childRule"] = request.GET.get("childRule")
    event["instagram"] = request.GET.get("instagram")
    event["twitter"] = request.GET.get("twitter")
    event["facebook"] = request.GET.get("facebook")
    event["youtube"] = request.GET.get("youtube")
    event["homepage"] = request.GET.get("homepage")
    event["starred"] = request.GET.get("starred")
    #event = urllib.parse.urlparse(data)
    print("event:", event["starred"])
    return render(request, "landing/detail.html", {"event": event})


