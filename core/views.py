from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login

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