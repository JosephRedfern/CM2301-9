from django.shortcuts import render
from learn.forms import *
from learn.models import Lecture, Module
from django.contrib.auth.decorators import login_required

@login_required
def create(request):
    form = LectureCreateForm()
    print form.as_p()
    return render(request, 'lecture_create.html', {'form': form})


@login_required
def view(request, lecture_id):
    values = {}
    values['lecture'] = Lecture.objects.get(pk=lecture_id)
    values['lectures'] = values['lecture'].module.lecture_set.all()
    values['modules'] = Module.objects.all()
    values['title'] = values['lecture'].title
    return render(request, 'lecture.html', values)
