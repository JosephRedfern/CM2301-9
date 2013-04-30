from django.shortcuts import render, get_object_or_404
from learn.models import *
from django.contrib.auth.decorators import login_required
from django.http import Http404


@login_required
def course(request, course_id):
    values = dict()

    values['course'] = get_object_or_404(Course, pk=course_id)

    if values['course'] in request.user.course.all():
        values['modules'] = values['course'].modules.all()
        values['title'] = values['course'].title+" - Modules"
        return render(request, "modules_overview.html", values)
    else:
        raise Http404