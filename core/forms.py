from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import UserProfile, Genre # don't use * here it will break shit

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

    class Meta:
        model = UserProfile
        fields = ["firstGenre", "secondGenre", "thirdGenre"]

    def __init__(self, *args, **kwargs):
        super(GenresForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)

        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()

            instance.genres.clear()

            data = self.cleaned_data

            for genre in GENRE_CHOICES:
                if genre[0] == data['firstGenre']:
                    genre_one = Genre.objects.filter(name = genre[1])[0]

                    break

            for genre in GENRE_CHOICES:
                if genre[0] == data['secondGenre']:
                    genre_two = Genre.objects.filter(name=genre[1])[0]

                    break

            for genre in GENRE_CHOICES:
                if genre[0] == data['thirdGenre']:
                    genre_three = Genre.objects.filter(name=genre[1])[0]

                    break

            instance.genres.add(genre_one)
            instance.genres.add(genre_two)
            instance.genres.add(genre_three)

        self.save_m2m = save_m2m

        instance.save()
        self.save_m2m()

        return instance

class PasswordReset(PasswordResetForm):
    class Meta:
        model = User
        fields = ["email"]

