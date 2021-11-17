from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Spotify_Notification_Cred(models.Model):
    has_spotify = models.CharField(max_length=5)
    username = models.CharField(max_length=50) 
    notifications = models.BooleanField(default = 1)

    def __str__(self):
        return '{},{}'.format(self.has_spotify, self.notifications)