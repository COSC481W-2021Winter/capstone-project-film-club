import json
import math
import requests
import random

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Sum

from .forms import *
from .models import *
from .templatetags import util



search_load_amount = 20
home_reviews_amount = 5

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

##INFO FOR MOVIES API##
#Docs https://www.themoviedb.org/
#Search for movies https://api.themoviedb.org/3/search/movie?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US&query=Star%20Wars&page=1&include_adult=false
#Search for Tv https://api.themoviedb.org/3/search/tv?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US&page=1&include_adult=false
#Search for actor https://api.themoviedb.org/3/search/person?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US&page=1&include_adult=false
#API functions we could maybe use: Get details, Get details, Get Popular

# Home/Landing Screen
def home(request):
    if not request.user.is_authenticated:  # Show landing page only when user is not logged in
        return render(request, 'core/landing.html', {
            # Data to return to template
        })

    recommendations = get_recommendations(request.user)
    recently_watched = list(request.user.userprofile.watched_movies.all())[-3:]
    reviews = json.loads(get_home_reviews(request).content)

    return render(request, 'core/home.html', {
        'recommendations': recommendations,
        'recently_watched': recently_watched,
        'reviews': reviews['reviews']
    })
def about(request):
    return render(request, 'core/about.html')

def bug_reporting_page(request):
    return render(request, 'core/bug_reporting_page.html')

def profile(request, username):
    reviews_json = []

    profile = User.objects.get(username = username)

    reviews = Review.objects.filter(user = profile).order_by('-added')
    watched_movies = profile.userprofile.watched_movies.all()[:3]
    following = profile.userprofile.following.all()[:6]
    followers = UserProfile.objects.filter(following = profile).all()[:6]

    for review in reviews:
        reviews_json.append(get_review_json(review, request.user))

    reviews_json = []
    profile_pic_form = ProfilePicForm()
    profile = User.objects.get(username = username)
    # Add the information from the register form...
    # form = Register
    reviews = Review.objects.filter(user = profile).order_by('-added')

    for review in reviews:
        reviews_json.append(get_review_json(review, request.user))

    # bio_form = BioForm()
    # if request.method == "POST":
    #     bio_form = BioForm(request.POST)
    #     if bio_form.is_valid():
    #         new_bio = bio_form.save()
    #         userprofile = UserProfile(user_bio = new_bio)
    #         userprofile.save()
    # else:
    #     bio_form = BioForm()

    return render(request, 'core/profile.html', {
        'profile': profile,
        'reviews': reviews_json,
        "profile_pic_form": profile_pic_form,
        'watched_movies': watched_movies,
        'following': following,
        'followers': followers,
        # "bio_form": bio_form
    })


def edit_profile(request, username):
    print(request.POST)

    if request.method == 'POST':
        if 'first-name' in request.POST or 'last-name' in request.POST or 'user-bio' in request.POST or 'privacy' in request.POST:
            first_name = request.POST.get('first-name')
            last_name = request.POST.get('last-name')
            bio = request.POST.get('user-bio')
            privacy = request.POST.get('privacy')

            if first_name is not None and len(first_name) > 0:
                request.user.first_name = first_name

            if last_name is not None and len(last_name) > 0:
                request.user.last_name = last_name

            if bio is not None and len(bio) > 0:
                request.user.userprofile.user_bio = bio

            if privacy is not None and len(privacy) > 0:
                request.user.userprofile.is_private = privacy == 'True'

            request.user.save()
            request.user.userprofile.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def review(request, review_id):
    review = Review.objects.filter(id = review_id)

    if not review.exists():
        return home(request)

    review = review[0]

    return render(request, 'core/review.html', {
        'review': get_review_json(review, request.user, False),
        'review_poster': review.user
    })

def review_like(request, review_id):
    data = {
        'success': True
    }

    review = Review.objects.filter(id=review_id)

    if review.exists():
        review = review[0]

        if review in request.user.userprofile.liked_reviews.all():
            request.user.userprofile.liked_reviews.remove(review)
        else:
            request.user.userprofile.liked_reviews.add(review)

        data['liked'] = review in request.user.userprofile.liked_reviews.all()
    else:
        data['success'] = False
        data['error_message'] = 'Review not found'

    return JsonResponse(data)

def review_comment(request, review_id):
    data = {
        'success': True
    }

    review = Review.objects.filter(id=review_id)

    if review.exists():
        review = review[0]

        comment = ReviewComment(user = request.user, review = review, text = request.POST.get('text'))
        comment.save()

        data['comment'] = {
            'user': {
                'username': request.user.username,
                'image_url': request.user.userprofile.profile_pic.url
            },
            'text': comment.text
        }
    else:
        data['success'] = False
        data['error_message'] = 'Review not found'

    return JsonResponse(data)

def movie(request, id):
    movie = get_movie(id)

    aggregate = {}

    review = None
    reviewed = False

    following_watched = request.user.userprofile.following.filter(userprofile__watched_movies = movie.pk)[:3]
    following_watched_other = request.user.userprofile.following.filter(userprofile__watched_movies=movie.pk)[3:]

    following_watched_count = following_watched_other.count()

    following_watched_string = ''

    if following_watched_other.count() > 0:
        following_watched_string = following_watched_other.all()[0].username

        for user in following_watched_other[1:]:
            following_watched_string += '&#x0a' + following_watched_other.all()[0].username

    if movie:
        # If user just reviewed the movie
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

        similar_movies = get_similar(id)

        # Aggregate work
        movie_reviews = Review.objects.filter(movie = movie)

        one_count = movie_reviews.filter(score__range = (1, 1.5)).count()
        two_count = movie_reviews.filter(score__range = (2, 2.5)).count()
        three_count = movie_reviews.filter(score__range = (3, 3.5)).count()
        four_count = movie_reviews.filter(score__range = (4, 4.5)).count()
        five_count = movie_reviews.filter(score = 5).count()

        review_count = movie_reviews.count() if movie_reviews.exists() else 1

        if movie_reviews.exists():
            aggregate['score'] = movie_reviews.aggregate(Sum('score'))['score__sum'] / review_count
        else:
            aggregate['score'] = 'N/A'

        aggregate['total'] = review_count
        aggregate['breakdown'] = {
            '1': {
                'amount': one_count,
                'proportion': float(one_count) / review_count * 100,
                'color': util.get_review_color(1)
            },
            '2': {
                'amount': two_count,
                'proportion': float(two_count) / review_count * 100,
                'color': util.get_review_color(2)
            },
            '3': {
                'amount': three_count,
                'proportion': float(three_count) / review_count * 100,
                'color': util.get_review_color(3)
            },
            '4': {
                'amount': four_count,
                'proportion': float(four_count) / review_count * 100,
                'color': util.get_review_color(4)
            },
            '5': {
                'amount': five_count,
                'proportion': float(five_count) / review_count * 100,
                'color': util.get_review_color(5)
            },
        }

        top_reviews = list(Review.objects.filter(movie = movie, user__userprofile__is_private = False).all())

        top_reviews.sort(key = lambda x: UserProfile.objects.filter(liked_reviews = x).count())
        top_reviews.reverse()

        top_reviews = top_reviews[:3]

        for i in range(len(top_reviews)):
            top_reviews[i] = get_review_json(top_reviews[i], request.user)

        if reviewed:
            review = get_review_json(review, request.user)

        return render(request, 'core/movie.html', {
            'movie': movie,
            'watched': request.user.userprofile.watched_movies.filter(pk = movie.pk).exists(),
            'review': review,
            'reviewed': reviewed,
            'similar_movies': similar_movies,
            'followers_watched': following_watched,
            'following_watched_other': following_watched_string,
            'following_watched_count': following_watched_other.count(),
            'aggregate': aggregate,
            'top_reviews': top_reviews
        })


def updateRecsNoTimer(request):
    return redirect('core:genres')

def search(request):
    data = {}

    results = []

    query = ''
    page = 1

    if request.method == 'GET':
        if 'q' in request.GET:
            query = request.GET['q']

        if 't' in request.GET:
            type = request.GET['t']

        if 'p' in request.GET:
            page = int(request.GET['p'])

        if type == 'movies':
            response = requests.get(
                'https://api.themoviedb.org/3/search/movie?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US&query=' + query + '&page=' + str(
                    page) + '&include_adult=false')

            raw_results = response.json()['results']

            for result in raw_results:
                results.append(create_movie(result))
        elif type == 'users':
            users = User.objects.filter(username__contains = query, userprofile__is_private = False)

            if users.exists():
                results = list(users.all())

    total_pages = math.ceil(len(results) / search_load_amount)

    lower_bound = page - 4 if page - 4 > 0 else 1
    upper_bound = page + 4 if page + 4 <= total_pages else total_pages

    shown_lower = (page - 1) * search_load_amount
    shown_upper = page * search_load_amount

    data['query'] = query
    data['type'] = type
    data['page_num'] = page

    data['total_pages'] = total_pages
    data['bound'] = range(lower_bound, upper_bound + 1)
    data['shown_lower'] = shown_lower + (1 if len(results) > 0 else 0)
    data['shown_upper'] = shown_lower + len(results[shown_lower:shown_upper])
    data['total_results'] = len(results)

    data['results'] = results[shown_lower:shown_upper]

    return render(request, 'core/search.html', data)

# https://www.techwithtim.net/tutorials/django/user-registration/
def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        profile_pic_form = ProfilePicForm(request.POST, request.FILES)

        if register_form.is_valid() and profile_pic_form.is_valid():
            new_user = register_form.save()

            if profile_pic_form.is_valid():
                pic = profile_pic_form.cleaned_data['profile_pic']
                if not pic:
                    pic = 'users/person_icon.png'

            userprofile = UserProfile(user = new_user, profile_pic = pic)
            userprofile.save()

            new_user = authenticate(username=register_form.cleaned_data['username'],
                                    password=register_form.cleaned_data['password1'],
                                    )

            login(request, new_user)

            return redirect("/welcome") #Disable until we find a work around.
            # return redirect("/genres")
    else:
        register_form = RegisterForm()
        profile_pic_form = ProfilePicForm()

    return render(request, "registration/register.html", {
        "register_form":register_form,
        "profile_pic_form": profile_pic_form})

@login_required
def welcome(request):
    user = request.user
    username = user.username
    subject = 'Welcome to FilmClub!'
    message = 'Hi ' + username + ', thank you for registering in FilmClub.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email, ]

    print("Email sent...")
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

def profile_picture_upload(request):
    if request.POST:
        print(request.FILES)

        profile_pic_form = ProfilePicForm(request.POST, request.FILES)
        # Add the information from the register form...
        # form = Register

        if profile_pic_form.is_valid():
            pic = request.FILES.get('profile-picture')

            if not pic:
                pic = 'users/person_icon.png'

            request.user.userprofile.set_profile_pic(pic)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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

def follow(request):
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

                if request.user.userprofile.following.filter(username = username).exists():
                    request.user.userprofile.following.remove(user)

                    data['added'] = False
                else:
                    request.user.userprofile.following.add(user)

                return JsonResponse(data)

    return JsonResponse({
        'success': False
    })

def get_followers(request, username):
    profile = User.objects.get(username = username)

    followers = UserProfile.objects.filter(following = profile).all()[6:]

    followers_json = []

    for follower in followers:
        followers_json.append({
            'username': follower.user.username,
            'profile_pic_url': follower.profile_pic.url,
            'profile_url': reverse('core:profile', kwargs = { 'username': follower.user.username })
        })

    return JsonResponse({
        'followers': followers_json
    })

def get_followees(request, username):
    profile = User.objects.get(username=username)

    followees = profile.userprofile.following.all()[6:]

    followees_json = []

    for followee in followees:
        followees_json.append({
            'username': followee.username,
            'profile_pic_url': followee.userprofile.profile_pic.url,
            'profile_url': reverse('core:profile', kwargs={'username': followee.username})
        })

    return JsonResponse({
        'followees': followees_json
    })

def get_movies(request, username):
    profile = User.objects.get(username=username)

    movies = profile.userprofile.watched_movies.all()[3:]

    movies_json = []

    for movie in movies:
        movies_json.append({
            'title': movie.title,
            'poster_url': movie.get_poster_url(),
            'movie_url': reverse('core:movie', kwargs={'id': movie.api_id})
        })

    return JsonResponse({
        'movies': movies_json
    })


def get_home_reviews(request, page = 1):
    reviews_json = []

    reviews = Review.objects.filter(user__in = request.user.userprofile.following.all()).order_by('-added').all()[(page - 1) * home_reviews_amount:page * home_reviews_amount]

    for review in reviews:
        reviews_json.append(get_review_json(review, request.user))

    return JsonResponse({
        'reviews': reviews_json,
        'page': page + 1,
        'more_to_load': len(reviews) == page * home_reviews_amount
    }, safe = False)

# Functions

def get_recommendations(user):
    recommendations = []
    rec_ids = []

    num_recommendations = 4

    genres = user.userprofile.genres.all()

    if len(genres) == 0:
        return recommendations

    recommendations_list = []

    for x in range(num_recommendations): 
        genre = genres[x % len(genres)].api_id

        response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=' + str(random.randint(1,100)) +'&with_genres=' + str(genre))
        results = response.json()['results']

        index = 0

        while index < 5:
            if index >= len(results):
                break

            if results[random.randint(0,3)]['id'] not in rec_ids:
                recommendations.append(create_movie(results[index]))
                rec_ids.append(results[index]['id'])

                break

            index += 1

    return recommendations
def get_similar(id):
    similar_movies = []

    response = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '/similar' + '?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US')
    results = response.json()['results']

    for result in results[:6]:
        similar_movies.append(create_movie(result))

    return similar_movies




def get_movie(id):
    movie = Movie.objects.filter(api_id=id)

    if movie.exists():
        return movie[0]

    response = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US')

    if response.status_code == 200:
        movie_json = response.json()

        return create_movie(movie_json)

    return None

def get_review_json(review, user, capped_comments = True, comment_cap = 2):
    comments = ReviewComment.objects.filter(review = review).order_by('-added')

    comments = list(comments.all())

    if capped_comments:
        comments = comments[:comment_cap]

    if capped_comments and len(comments) == 2:
        temp_comment = comments[0]

        comments[0] = comments[1]
        comments[1] = temp_comment

    for x in range(len(comments)):
        comment = comments[x]

        comments[x] = {
            'user': {
                'username': comment.user.username,
                'image_url': comment.user.userprofile.profile_pic.url
            },
            'text': comment.text
        }

    return {
        'id': review.id,
        'user': {
            'username': review.user.username,
            'image_url': review.user.userprofile.profile_pic.url
        },
        'movie': {
            'id': review.movie.get_absolute_id(),
            'title': review.movie.title,
            'description': review.movie.description,
            'poster_url': review.movie.get_poster_url()
        },
        'score': review.score,
        'title': review.title,
        'text': review.text,
        'added': util.get_normal_time(str(review.added)),
        'liked': review in user.userprofile.liked_reviews.all(),
        'like_count': UserProfile.objects.filter(liked_reviews = review).count(),
        'comment_count': ReviewComment.objects.filter(review = review).count(),
        'comments': comments
    }

def create_movie(movie_json):
    movie = Movie.objects.filter(api_id=movie_json['id'])

    if movie.exists():
        movie = movie[0]
    else:
        movie = Movie(title=movie_json['title'], description=movie_json['overview'], api_id=movie_json['id'],
                      poster_path=movie_json['poster_path'])
        movie.save()

        movie_genres = movie_json['genres'] if 'genres' in movie_json else movie_json['genre_ids']

        alt_genre = False

        if 'genre_ids' in movie_json:
            alt_genre = True

        for movie_genre in movie_genres:
            if alt_genre:
                genre = Genre.objects.filter(api_id=movie_genre)
            else:
                genre = Genre.objects.filter(api_id=movie_genre['id'])

            if genre.exists():
                genre = genre[0]
            else:
                try:
                    genre = Genre(name=movie_genre['name'], api_id=movie_genre['id'])
                except:
                    genre = Genre(name='Not Available', api_id=movie_genre)

                genre.save()

            movie.genres.add(genre)

    return movie

def error_404(request, exception):
    return render('404.html')
def error_500(request):
    return render('500.html')
def error_403(request, exception):
    return render('403.html')
def error_400(request, exception):
    return render('400.html')

def edit_user_bio(request):
    if request.POST:
        bio_form = BioForm(request.POST)

        if bio_form.is_valid():
            bio = request.POST.get('user-bio')

            request.user.userprofile.set_user_bio(bio)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
