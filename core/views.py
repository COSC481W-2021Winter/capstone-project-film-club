import json
import math
import requests

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

    response = requests.get(
        'https://api.themoviedb.org/3/genre/movie/list?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US')
    results = response.json()

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
    for review in reviews:
        reviews_json.append(get_review_json(review))
    if request.method == "POST":
        profile_pic_form = ProfilePicForm(request.POST, request.FILES)
        # Add the information from the register form...
        # form = Register

        if profile_pic_form.is_valid():
                    pic = profile_pic_form.cleaned_data['profile_pic']
                    if not pic:
                        pic = 'users/person_icon.png'
        userprofile = UserProfile(user=profile, profile_pic = pic)
        userprofile.set_profile_pic(pic)

        return render(request, 'core/profile.html', {
            'profile': profile,
            'reviews': reviews_json
        })
    else:
        reviews_json = []
        profile_pic_form = ProfilePicForm()
        profile = User.objects.get(username = username)
        # Add the information from the register form...
        # form = Register
        reviews = Review.objects.filter(user = profile).order_by('-added')

        for review in reviews:
            reviews_json.append(get_review_json(review))

        return render(request, 'core/profile.html', {
            'profile': profile,
            'reviews': reviews_json,
            "profile_pic_form": profile_pic_form
        })


def edit_profile(request, username):
    if request.method == 'POST':
        if 'first-name' in request.POST and 'last-name' in request.POST:
            first_name = request.POST.get('first-name')
            last_name = request.POST.get('last-name')

            if len(first_name) > 0 and len(last_name) > 0:
                request.user.first_name = first_name
                request.user.last_name = last_name

                request.user.save()

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

    friends = request.user.userprofile.friends.filter(pk = movie.pk)

    fstring = "None of your friends have watched this"

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

        if friends.count() > 0:
            fstring = friend[0].username + " has watched this"

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

        review = get_review_json(review, request.user)

        return render(request, 'core/movie.html', {
            'movie': movie,
            'watched': request.user.userprofile.watched_movies.filter(pk = movie.pk).exists(),
            'review': review,
            'reviewed': reviewed,
            'similar_movies': similar_movies,
            'fstring': fstring,
            'aggregate': aggregate
        })

def search(request):
    data = {}

    query = ''
    page = 1

    if request.method == 'GET':
        if 'search_user_or_movie' in request.GET:
            search_user_or_movie = str(request.GET['search_user_or_movie'])

            if search_user_or_movie == "PrivacySetting":
                if UserProfile.isPrivate:
                    UserProfile.isPrivate = False
                else:
                    UserProfile.isPrivate = True
                if 'q' in request.GET:
                    query = ''
                    data['query'] = str(UserProfile.__name__) + " is now " + str(UserProfile.isPrivate)
                    try:
                        out_put = User.objects.get(username=str(query))
                        data['res_u'] = User.objects.all()
                        data['res_top'] = out_put 
                        linkMaker = data['res_top'] + " %}"
                        data['data_url_two'] = "{% url 'core:profile' ascha %}"
                        data['data_url'] = "{% url 'core:profile' user.username %}"
                        return render(request, 'core/search.html', data)
                        #return redirect('core:home')
                    except:
                        #return redirect('core:home')
                        return render(request, 'core/search.html', data)



            if search_user_or_movie == "Users":
                if 'q' in request.GET:
                    query = request.GET['q']
                    data['query'] = request.GET['q']


                    #out_put = User.objects.get(username="asch")
                    try:
                        out_put = User.objects.get(username=str(query))
                        data['query'] = str(out_put) + " ---------- " + str()
                        data['res_u'] = User.objects.all()
                        data['res_top'] = out_put 
                        linkMaker = data['res_top'] + " %}"
                        data['data_url_two'] = "{% url 'core:profile' ascha %}"
                        data['data_url'] = "{% url 'core:profile' user.username %}"
                        data['query'] = str(out_put.isPrivate)
                        return render(request, 'core/search.html', data)
                    except:
                        return render(request, 'core/search.html', data)
                    
                    #out_put = User.objects.get(username=)
                
                
                #data['res'] = UserProfile.objects.all() #querey set can not be made into json
                #data['res_u'] = User.objects.all()
                #trey
                #data['res_u'] = 
                
                #out_put = User.objects.get(username="asch")
                #out_put_list = []
                #data['res_m'] = out_put_list.append(out_put)
                
                
                #data['res_m'] = Movie.objects.all()
                data['query'] = request.GET['q']
                data['res_top'] = out_put
                #data['res_top'] = User.objects.get(first_name='Alex')
                #return render(request, 'core/search.html', data)

    

    if request.method == 'GET':
        if 'q' in request.GET:
            query = request.GET['q']

        if 'p' in request.GET:
            page = int(request.GET['p'])

        response = requests.get('https://api.themoviedb.org/3/search/movie?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US&query=' + query + '&page=' + str(page) + '&include_adult=false')
        raw_results = response.json()['results']

        print('\n\n\n' + str(len(raw_results)))

        results = []

        for result in raw_results:
            results.append(create_movie(result))

    '''
    return_data_for_users_one = User.objects.all()
    return_data_for_users = UserProfile.objects.all()
    '''
    #print(return_data_for_users)

    #return_data_for_users = Movie.objects.all()
    #user = User.objects.get(username='asc')
    #return_data_for_users = UserProfile.objects.all()

    total_pages = math.ceil(len(results) / search_load_amount)

    lower_bound = page - 4 if page - 4 > 0 else 1
    upper_bound = page + 4 if page + 4 <= total_pages else total_pages

    shown_lower = (page - 1) * search_load_amount
    shown_upper = page * search_load_amount

    data['query'] = query
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
    email_from = settings.EMAIL_HOST_USER
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

def get_home_reviews(request, page = 1):
    reviews_json = []

    reviews = Review.objects.filter(user__userprofile__friends = request.user).order_by('-added').all()[(page - 1) * home_reviews_amount:page * home_reviews_amount]

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
def get_similar(id):
    similar_movies = []

    response = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '/similar' + '?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US')
    results = response.json()['results']
    index = 0
    while index < 4:
        similar_movies.append(create_movie(results[index]))
        index += 1

    return similar_movies




def get_movie(id):
    response = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '?api_key=a1a486ad19b99d238e92778b9ceb4bb4&language=en-US')

    if response.status_code == 200:
        movie_json = response.json()

        return create_movie(movie_json)

    return None

def get_review_json(review, user, capped_comments = True, comment_cap = 2):
    comments = ReviewComment.objects.filter(review = review).order_by('-added')

    if capped_comments:
        comments = comments[:comment_cap]

    comments = list(comments.all())

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