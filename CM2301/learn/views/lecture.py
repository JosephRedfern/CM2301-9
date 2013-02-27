from django.shortcuts import render
from learn.forms import *
from django.contrib.auth.decorators import login_required

@login_required
def create(request):
    form = LectureCreateForm()
    print form.as_p()
    return render(request, 'lecture_create.html', {'form': form})