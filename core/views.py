from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login 
from django.conf import settings 
from django.core.mail import send_mail 
from .forms import *
from .models import *
from django.core.checks import messages
from django.contrib.auth.decorators import login_required

#Landing Screen
def index(request):
    return render(request, 'core/index.html', {
        # Data to return to template
    })

#Home Screen
def home(request):
    return render(request, 'core/home.html', {
        # Data to return to template
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