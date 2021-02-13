from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genres = models.ManyToManyField('Genre', blank = True, related_name = 'genres')

class Genre(models.Model):
    name = models.CharField(max_length = 50)
    api_id = models.IntegerField()