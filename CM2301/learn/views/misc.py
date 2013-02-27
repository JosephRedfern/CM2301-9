from django.shortcuts import render, redirect
from learn.models import Video, User
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from learn.forms import *

@login_required
def home(request):
    values = {}
    values['title'] = 'Home'
    return render(request, 'base_navbar.html', values)


def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        return login(request, template_name='login.html')
    