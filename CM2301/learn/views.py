from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import Http404
from learn.models import Video, User
from learn.forms import *

@login_required
def home(request):
    values = {}
    values['title'] = 'Home'
    return render(request, 'base_navbar.html', values)

def video_create(request):
    form = VideoUploadForm()
    videos = Video.objects.all()
    return render(request, 'video_upload.html', {'videos': videos, 'form': form})

def videos(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})


def video(request, video_id):
    print video_id
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        raise Http404('Video %s does not exist' % (video_id))
    print video.uploaded_video
    return render(request, 'video_player.html', {'video': video})
            

def video_submit(request, video_id):
    if request.method == 'POST':
        form = VideoUploadForm(data=request.POST, files=request.FILES)
        
        if form.is_valid():
            form.save()
            return HttpResponse("MOTHER FUCKER IT UPLOADED")
        
def serve_video(request, video_id):
    video = Video.objects.get(pk=video_id)
    print video.uploaded_video.url
    filename = video.uploaded_video.name.split('/')[-1]
    response = HttpResponse(video.uploaded_video, content_type='video/mp4')
    print video.uploaded_video.file.size
    response['Content-length'] = video.uploaded_video.file.size
    

    return response
    

def login(request):
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

        
def lecture_create(request):
    form = LectureCreateForm()
    print form.as_p()
    return render(request, 'lecture_create.html', {'form': form})