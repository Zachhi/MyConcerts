from django.contrib import admin
from . import models
#displayed and modified via admin

class Spotify_Notification_CredAdmin(admin.ModelAdmin):
    pass 

admin.site.register(models.Spotify_Notification_Cred, Spotify_Notification_CredAdmin)

class Starred_Concerts_Admin(admin.ModelAdmin):
    pass 

admin.site.register(models.Starred_Concerts, Starred_Concerts_Admin)