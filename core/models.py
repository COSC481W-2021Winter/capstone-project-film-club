from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)

class Favorites(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstGenre = models.CharField(max_length=50)
    secondGenre = models.CharField(max_length=50)
    thirdGenre = models.CharField(max_length=50)