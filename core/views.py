import requests

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import *
from .models import *

# Home/Landing Screen
def home(request):
    if not request.user.is_authenticated:  # Show landing page only when user is not logged in
        return render(request, 'core/landing.html', {
            # Data to return to template
        })

    recommendations = get_recommendations(request.user)

    for rec in recommendations:
        rec['poster_url'] = 'https://image.tmdb.org/t/p/w500' + rec['poster_path']

    return render(request, 'core/home.html', {
        'recommendations': recommendations
    })

def profile(request, username):
    profile = User.objects.get(username = username)

    return render(request, 'core/profile.html', {
        'profile': profile
    })

def movie(request, id):
    movie = get_movie(id)

    if movie:
        movie['poster_url'] = get_poster_url(movie)

        return render(request, 'core/movie.html', {
            'movie': movie
        })

#https://www.techwithtim.net/tutorials/django/user-registration/
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect("/welcome")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form":form})

@login_required
def welcome(request):
    user = request.user
    username = user.username
    subject = 'Welcome to FilmClub!'
    message = 'Hi '+username+', thank you for registering in FilmClub.'
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [user.email, ] 
    send_mail( subject, message, email_from, recipient_list )
    return redirect("/genres") 

def genres(request):
    user = request.user
    if request.method == "POST": #Check if incoming request is submited form
        form = GenresForm(request.POST) #Decide what form to use form forms.py
        if form.is_valid(): #if this is a valid response
            genres = form.save(commit=False)
            genres.user = request.user
            genres.save() #Save to the database
            return redirect("/home") #redirect the user to the home page
    else: #this is not a submited form
        form = GenresForm() #set the form form forms.py
    return render(request, 'core/genres.html', {"form":form}) #return the correct form for page

def reset(request):
    if request.method == "POST":
        form = PasswordReset(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/sent")
    else:
        form = PasswordReset(request.POST)
    return render(request, 'registration/password_reset.html', {"form":form})

def sent(request):
    return render(request, 'registration/password_reset_sent.html', {
        # Data to return to template
    })

# Functions

def get_recommendations(user):
    recommendations = []

    genres = [28, 12, 10752, 53]

    for genre in genres:
        response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres=' + str(genre))
        results = response.json()['results']

        index = 0

        while True:
            if results[index] not in recommendations:
                recommendations.append(results[index])

                break

            index += 1

    return recommendations

def get_movie(id):
    response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1')
    results = response.json()['results']

    if len(results) > 0:
        return results[0]

    return None

def get_poster_url(movie):
    return 'https://image.tmdb.org/t/p/w500' + movie['poster_path']