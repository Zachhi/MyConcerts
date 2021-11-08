from django.shortcuts import render
import requests
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
    response = requests.get('https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&countryCode=US&apikey=HCme8Zo9DSUpVKCGGF9CbgcTKO3YbsjE&page=1') 
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

def home(request):
    response = requests.get('https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&countryCode=US&apikey=HCme8Zo9DSUpVKCGGF9CbgcTKO3YbsjE&page=1') 
    # try changing p = 2!!!!!!!!!!!!! on line above
    # super easy pagination-type querying 

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
        dictionary["image"] = e["images"][1]["url"]
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
    return render(request, "landing/home.html", {"events": events})
    # events has elements name, url, image, date, time, venue, city, state, min_price, max_price



def about(request):
    return render(request, 'landing/about.html', {'title':'About'}) 