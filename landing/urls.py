from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('spotify-auth', views.spotify_auth, name='spotify-auth'),
    path('callback', views.callback, name = 'callback'),
    path('', views.login_home, name='login-home'),
    path('<int:page>/', views.home, name='landing-home'),
    path('0/', views.home, name='landing-home-default'),
    path('about/', views.about, name='landing-about'),
    path('details/', views.detail, name='landing-detail'),
    path('add_star/', views.add_star, name = 'add_star'),
    path('remove_star/', views.remove_star, name = 'remove_star'),
    #path('get_starred_concerts', views.get_starred_concerts, name = 'get_starred_concerts'),
    path('change-username/', views.change_username, name = 'change-username'),
    path('change-notifications/', views.change_notifications, name = 'change-notif'),
    path('settings-main/', views.settings_main, name = 'settings-main'),
    
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='landing/change-password.html',
            success_url = '/'
        ),
        name='change_password'
    ),
    
]