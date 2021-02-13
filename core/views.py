import requests
from django.http import JsonResponse

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
    recently_watched = list(request.user.userprofile.watched_movies.all())[-3:]

    return render(request, 'core/home.html', {
        'recommendations': recommendations,
        'recently_watched': recently_watched
    })

def profile(request, username):
    profile = User.objects.get(username = username)

    return render(request, 'core/profile.html', {
        'profile': profile
    })

def movie(request, id):
    movie = get_movie(id)
    review = None

    reviewed = False

    if movie:
        if request.POST:
            title = request.POST.get('title')
            score = request.POST.get('score')
            text = request.POST.get('text')

            if not Review.objects.filter(user = request.user, movie = movie).exists() and title and score and text:
                review = Review(user = request.user, movie = movie, title = title, score = score, text = text)
                review.save()

                reviewed = True

        if not reviewed:
            review = Review.objects.filter(user=request.user, movie=movie)

            if review.exists():
                review = review[0]

                reviewed = True

        return render(request, 'core/movie.html', {
            'movie': movie,
            'watched': request.user.userprofile.watched_movies.filter(pk = movie.pk).exists(),
            'review': review,
            'reviewed': reviewed
        })

def add_movie(request):
    if request.POST:
        pass

    return render(request, 'core/addmovie.html')

# https://www.techwithtim.net/tutorials/django/user-registration/
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save()

            userprofile = UserProfile(user = new_user)
            userprofile.save()

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
    message = 'Hi ' + username + ', thank you for registering in FilmClub.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]

    send_mail(subject, message, email_from, recipient_list)

    return redirect("/genres") 

def genres(request):
    user = request.user

    if request.method == "POST":  # Check if incoming request is submitted form
        form = GenresForm(request.POST, instance = request.user.userprofile)  # Decide what form to use form forms.py

        if form.is_valid():  # if this is a valid response
            genres = form.save(commit=False)
            genres.user = request.user
            genres.save()  # Save to the database

            return redirect('core:home')  # redirect the user to the home page
    else:  # this is not a submited form
        form = GenresForm()  # set the form form forms.py

    return render(request, 'core/genres.html', {"form":form})  # return the correct form for page

def reset(request):
    if request.method == "POST":
        form = PasswordReset(request.POST)

        if form.is_valid():
            form.save()

            return redirect("/sent")
    else:
        form = PasswordReset(request.POST)

    return render(request, 'registration/password_reset.html', {"form": form})

def sent(request):
    return render(request, 'registration/password_reset_sent.html', {
        # Data to return to template
    })

def watch(request):
    if request.POST:
        movie_id = request.POST['movie_id']

        if movie_id:
            movie = Movie.objects.filter(api_id = movie_id)

            print(movie_id)

            if movie:
                movie = movie[0]
            else:
                movie = Movie.objects.filter(user_added = True, id = movie_id)

                print(movie)

                if movie:
                    movie = movie[0]
                else:
                    movie = get_movie(movie_id)

                    if not movie:
                        return JsonResponse({
                            'success': False
                        })

            data = {
                'success': True,
                'added': True
            }

            if request.user.userprofile.watched_movies.filter(pk = movie.pk):
                request.user.userprofile.watched_movies.remove(movie)

                data['added'] = False
            else:
                request.user.userprofile.watched_movies.add(movie)

            return JsonResponse(data)

    return JsonResponse({
        'success': False
    })

def friend(request):
    if request.POST:
        username = request.POST['username']

        if username:
            user = User.objects.filter(username = username)

            if user:
                user = user[0]

                data = {
                    'success': True,
                    'added': True
                }

                if request.user.userprofile.friends.filter(username = username).exists():
                    request.user.userprofile.friends.remove(user)

                    data['added'] = False
                else:
                    request.user.userprofile.friends.add(user)

                return JsonResponse(data)

    return JsonResponse({
        'success': False
    })

# Functions

def get_recommendations(user):
    recommendations = []
    rec_ids = []

    num_recommendations = 4

    genres = user.userprofile.genres.all()

    if len(genres) == 0:
        return recommendations

    for x in range(num_recommendations):
        genre = genres[x % len(genres)].api_id

        response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres=' + str(genre))
        results = response.json()['results']

        index = 0

        while True:
            if index >= len(results):
                break

            if results[index]['id'] not in rec_ids:
                recommendations.append(create_movie(results[index]))
                rec_ids.append(results[index]['id'])

                break

            index += 1

    return recommendations

def get_movie(id):
    response = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US')

    if response.status_code == 200:
        movie_json = response.json()

        return create_movie(movie_json)

    return None

def create_movie(movie_json):
    movie = Movie.objects.filter(api_id=movie_json['id'])

    if movie.exists():
        movie = movie[0]
    else:
        movie = Movie(title=movie_json['title'], description=movie_json['overview'], api_id=movie_json['id'],
                      poster_path=movie_json['poster_path'])
        movie.save()

        for movie_genre in movie_json['genres']:
            genre = Genre.objects.filter(api_id=movie_genre['id'])

            if genre.exists():
                genre = genre[0]
            else:
                genre = Genre(name=movie_genre['name'], api_id=movie_genre['id'])
                genre.save()

            movie.genres.add(genre)

    return movie

def get_poster_url(movie):
    return 'https://image.tmdb.org/t/p/w500' + movie.poster_path