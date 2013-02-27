from django.shortcuts import render
from learn.models import Video, User, Module
from learn.forms import *

def home(request):
    values = {}
    values['title'] = 'Home'
    values['modules'] = Module.objects.all()
    print values['modules']
    return render(request, 'base_navbar.html', values)
