from django.shortcuts import render, redirect
from learn.forms import *
from learn.models import Lecture, Module, Link
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import uuid
from django.core.exceptions import PermissionDenied

@login_required
def create(request, module_id):

    if not request.user.is_staff:
        raise PermissionDenied()

    values = {}
    values['modules'] = Module.objects.all()

    if request.method == 'POST':
        video_form = VideoForm(request.POST, request.FILES, prefix='video')
        lecture_form = LectureForm(request.POST, prefix='lecture')
        print "Video form valid: " + video_form.as_p()
        print video_form.is_valid()
        if all([lecture_form.is_valid(), video_form.is_valid()]):
            video = video_form.save(commit=False)
            lecture = lecture_form.save(commit=False)
            video.id = uuid.uuid4().hex
            lecture.video = video
            video.save()
            lecture.save()
            
            return redirect(lecture.get_absolute_url())
    
    lecture_form = LectureForm(prefix="lecture", initial={'module': module_id})
    video_form = VideoForm(prefix="video")
    values['lecture_form'] = lecture_form
    values['video_form'] = video_form
    print lecture_form.as_p()
    return render(request, 'lecture_create.html', values)


@login_required
def view(request, lecture_id):
    attachment_form = AttachmentForm(prefix='attachment', initial={'object_id': lecture_id})
    revision_form = RevisionForm(prefix='revision')
    Viewed.log_view(request, lecture_id)
    values = {}
    values['lecture'] = Lecture.objects.get(pk=lecture_id)
    values['lectures'] = values['lecture'].module.lecture_set.all()
    values['modules'] = Module.objects.all()
    values['title'] = values['lecture'].title
    values['attachments'] = Attachment.objects.filter(object_id=lecture_id)
    values['links'] = Link.objects.filter(object_id=lecture_id)
    values['test'] = Test.objects.filter(lecture=values['lecture']) 
    values['test_results'] = TestInstance.objects.filter(test=values['test'], student=request.user)
    values['attachment_form'] = attachment_form
    values['revision_form'] = revision_form

    courses = request.user.course.all()
    if not set(courses) & set(values['lecture'].module.courses.all()):
        print "sdfdf"
        raise PermissionDenied()


    values['breadcrumb'] = ('LCARS', values['lecture'].module.title + " ("+values['lecture'].module.module_code+')', values['lecture'].title)
    return render(request, 'lecture.html', values)

