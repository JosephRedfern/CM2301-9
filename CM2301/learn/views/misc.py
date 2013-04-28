from django.shortcuts import render, redirect
from learn.models import Video, User, Announcement
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from learn.forms import *

@login_required
def home(request):
    values = {}
    values['title'] = 'Home'
    values['modules'] = Module.objects.all()
    values['announcements'] = Announcement.objects.all()[:5]
    viewed = Viewed.objects.filter(user=request.user)
    values['activity'] = []

    values['breadcrumb'] = ("LCARS", "Overview")
    return render(request, 'overview.html', values)


def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        return login(request, template_name='login.html')
    
