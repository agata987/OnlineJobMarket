from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import *


def home_page(request):
    return render(request, 'jobSite_app/home.html')
