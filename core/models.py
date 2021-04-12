from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genres = models.ManyToManyField('Genre', blank = True, related_name = 'genres')
    profile_pic = models.ImageField(default='users/person_icon.png', null=True, blank=True, upload_to="users/")
    watched_movies = models.ManyToManyField('Movie', blank = True, related_name = 'watched_movies')
    liked_reviews = models.ManyToManyField('Review', blank = True, related_name = 'liked_reviews')
    following = models.ManyToManyField(User, blank = True, related_name = 'friends')
    isPrivate = False

    def set_profile_pic(self, pic):
        self.profile_pic = pic

class Genre(models.Model):
    name = models.CharField(max_length = 50)
    api_id = models.IntegerField()

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 1000)
    user_added = models.BooleanField(default = False)
    api_id = models.IntegerField()
    poster_path = models.CharField(max_length = 100, blank = True, null = True)
    genres = models.ManyToManyField('Genre', blank = True, related_name = 'movie_genres')

    def __str__(self):
        return self.title

    def get_poster_url(self):
        return None if self.poster_path is None else 'https://image.tmdb.org/t/p/w500' + self.poster_path

    def get_absolute_id(self):
        return self.pk if self.user_added else self.api_id

class Review(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    text = models.TextField()
    score = models.FloatField()
    added = models.DateTimeField(auto_now_add = True)

class ReviewComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    added = models.DateTimeField(auto_now_add = True)