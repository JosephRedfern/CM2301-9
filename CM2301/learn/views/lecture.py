from django.shortcuts import render
from learn.forms import *

def create(request):
    form = LectureCreateForm()
    print form.as_p()
    return render(request, 'lecture_create.html', {'form': form})