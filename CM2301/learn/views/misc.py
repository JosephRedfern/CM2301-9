from django.shortcuts import render
from learn.models import Video, User
from learn.forms import *

def home(request):
    values = {}
    values['title'] = 'Home'
    return render(request, 'base_navbar.html', values)
