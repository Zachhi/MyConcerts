from django.shortcuts import render

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
    context = {
        'posts': post
    }
    return render(request, 'landing/home.html', context) 

def about(request):
    return render(request, 'landing/about.html', {'title':'About'}) 