from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login
from .forms import *

from .models import *

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
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/genres")
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form":form})

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