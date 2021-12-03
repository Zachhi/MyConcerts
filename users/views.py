from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

#from landing.views import spotify_auth
from users.models import Spotify_Notification_Cred

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            spotify = form.cleaned_data.get('spotify')
            # save username into spotifycred model
            s1 = Spotify_Notification_Cred(username = username, has_spotify = spotify)
            s1.save()
            #print(spotify)
            messages.success(request, f'Account created for {username}!')
            return redirect('login')     #first of all havent tested if the has_spotify was actually passed to the template.. and theres a problem with a user who is just logging in
                                                                #... a user who is logging in and already has registered before wouldn't get that flag set for has_spotify.. so we need to store it

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    notification_prf = Spotify_Notification_Cred.objects.get(username=request.user)
    notification_prf = notification_prf.notifications
    return render(request, 'users/profile.html', {"notifications":str(notification_prf)})

