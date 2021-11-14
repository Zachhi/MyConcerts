from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class SpotifyCred(models.Model):
    has_spotify = models.CharField(max_length=5)
    username = models.CharField(max_length=50) #reference 