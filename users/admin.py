from django.contrib import admin
from . import models
#displayed and modified via admin

class SpotifyCredAdmin(admin.ModelAdmin):
    pass 

admin.site.register(models.SpotifyCred, SpotifyCredAdmin)