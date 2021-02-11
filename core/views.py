import requests
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login
from .forms import RegisterForm

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

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)

        if form.is_valid():
            form.save()

            return redirect("core:home")
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {
        "form": form
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