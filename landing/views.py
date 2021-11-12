from django.shortcuts import render
import requests
from datetime import date
'''
post = [
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted:': 'August 28, 2018'
    }
]

def home(request):
    response = requests.get('https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&countryCode=US&apikey=HCme8Zo9DSUpVKCGGF9CbgcTKO3YbsjE&page=200') 
    # try changing p = 2!!!!!!!!!!!!! on line 12
    # super easy pagination-type querying 
    concerts = response.json()
    concerts = concerts["_embedded"]
    events = concerts["events"]
    return render(request, "landing/home.html", {"events": events})

    context = {
        'posts': post
    }
    return render(request, 'landing/home.html', context)
'''

def login_home(request):
    return render(request, "landing/loginhome.html")

def home(request, page): 

    events = ticket_master_request(page=page)
    return render(request, "landing/home.html", {"events": events, "page": page})
    # events has elements name, url, image, date, time, venue, city, state, min_price, max_price

def ticket_master_request(genre = '', city = '', page = 1, start_date = date.today().strftime("%Y-%m-%d"), end_date = '2022-12-25'):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json?&countryCode=US&apikey=HCme8Zo9DSUpVKCGGF9CbgcTKO3YbsjE&page=' + str(page)
    if(city != ''):
        url = url + '&city=' + city
    if(genre != ''):
        url = url + '&classificationName=' + genre
    if(start_date != ''):
        url = url + '&startDateTime=' + start_date + 'T00:00:00Z'
    if(end_date != ''):
        url = url + '&endDateTime=' + end_date + 'T00:00:00Z'

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
        if(e["dates"]["start"]["dateTBA"] == False):
            dictionary["date"] = e["dates"]["start"]["localDate"]
        else:
            dictionary["date"] = "TBA"
        
        if(e["dates"]["start"]["timeTBA"] == False):
            dictionary["time"] = e["dates"]["start"]['localTime']
        else: 
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
            
        events.append(dictionary)

    return events

def about(request):
    return render(request, 'landing/about.html', {'title':'About'}) 