from django.urls import path
from . import views

urlpatterns = [
    path('spotify-auth', views.spotify_auth, name='spotify-auth'),
    path('callback', views.callback, name = 'callback'),
    path('landing/home', views.home, name='landing-home'),
    path('about/', views.about, name='landing-about'),
]