from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from learn.models import Video, User
from learn.forms import *

@login_required
def home(request):
    values = {}
    values['title'] = 'Home'
    return render(request, 'base_navbar.html', values)


def videos(request):
    form = VideoUploadForm()
    videos = Video.objects.all()
    return render(request, 'video_upload.html', {'videos': videos, 'form': form})

def video_submit(request):
    if request.method == 'POST':
        form = VideoUploadForm(data=request.POST, files=request.FILES)
        
        if form.is_valid():
            form.save()
            return HttpResponse("MOTHER FUCKER IT UPLOADED")

def login(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})
