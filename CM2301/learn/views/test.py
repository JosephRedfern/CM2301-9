from django.shortcuts import render
from learn.forms import *
from learn.models import Lecture, Module, Link
from django.contrib.auth.decorators import login_required

@login_required
def test(request,test_id):

    values = {}
    values['sf'] = "af"

    return render(request, "test.html", values)
