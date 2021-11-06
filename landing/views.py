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
'''
def home(request):
    response = requests.get('https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&countryCode=US&apikey=HCme8Zo9DSUpVKCGGF9CbgcTKO3YbsjE&page=1') 
    # try changing p = 2!!!!!!!!!!!!! on line 12
    # super easy pagination-type querying 
    concerts = response.json()
    concerts = concerts["_embedded"]
    events = concerts["events"]
    return render(request, "landing/home.html", {"events": events})

    '''
    context = {
        'posts': post
    }
    return render(request, 'landing/home.html', context)
    ''' 

def about(request):
    return render(request, 'landing/about.html', {'title':'About'}) 