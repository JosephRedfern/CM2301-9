from django.shortcuts import render
from django.http import HttpResponse
from learn.models import Video
from learn.forms import *

def home(request):
    return render(request, 'base_navbar.html')


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