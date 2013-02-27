from django.shortcuts import render, redirect
from learn.models import Video, User
from django.contrib.auth.views import login
from learn.forms import *

def home(request):
    values = {}
    values['title'] = 'Home'
    return render(request, 'base_navbar.html', values)


def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        return login(request, template_name='login.html')
    