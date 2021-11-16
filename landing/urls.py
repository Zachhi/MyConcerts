from django.urls import path
from . import views

urlpatterns = [
    path('spotify-auth', views.spotify_auth, name='spotify-auth'),
    path('callback', views.callback, name = 'callback'),
    path('', views.login_home, name='login-home'),
    path('<int:page>/', views.home, name='landing-home'),
    path('1/', views.home, name='landing-home-default'),
    path('about/', views.about, name='landing-about'),
    path('details/', views.detail, name='landing-detail'),
]