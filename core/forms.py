from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

GENRE_CHOICES = (
    ('AC', 'Action'),
    ('AD', 'Adventure'),
    ('AN', 'Animation'),
    ('CO', 'Comedy'),
    ('CR', 'Crime'),
    ('DO', 'Documentary'),
    ('DR', 'Drama'),
    ('FA', 'Family'),
    ('FY', 'Fantasy'),
    ('HO','History'),
    ('HR','Horror'),
    ('MU', 'Music'),
    ('MY','Mystery'),
    ('RO','Romance'),
    ('SF', 'Science Fiction'), 
    ('TH','Thriller'),
    ('WA', 'War'),
    ('WE', 'Western'),
)

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class GenresForm(forms.ModelForm):
    firstGenre = forms.CharField(label="What is your favorite genre?", widget=forms.Select(choices=GENRE_CHOICES))
    secondGenre = forms.CharField(label="What is your second favorite genre?", widget=forms.Select(choices=GENRE_CHOICES))
    thirdGenre = forms.CharField(label="What is your third favorite genre?", widget=forms.Select(choices=GENRE_CHOICES))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(GenresForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Favorites
        fields = ["firstGenre", "secondGenre", "thirdGenre"]


