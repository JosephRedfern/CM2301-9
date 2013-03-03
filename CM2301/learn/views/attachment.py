from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from learn.models import Attachment, Revision, Module
from learn.forms import *
import mimetypes


def attachment(request, attachment_id):
    values = {}
    values['attachment'] = Attachment.objects.get(id=attachment_id)
    values['title'] = "Attachment %s"%(values['attachment'].file_name)
    values['modules'] = Module.objects.all()
    return render(request, 'attachment.html', values)

@require_http_methods(["GET"])
@login_required
def revision_delete(request, revision_id):
    revision = Revision.objects.get(pk=revision_id)
    if len(revision.attachment.revision_set.all()) < 2:
        messages.warning(request, 'Revision not deleted')
        return redirect(revision.attachment.get_absolute_url())
    
    revision.delete()
    messages.success(request, 'Revision Deleted')
    return redirect(revision.attachment.get_absolute_url())
    
def revision(request, revision_id):
    revision = Revision.objects.get(pk=revision_id)
    revision.delete()
    
def revision_download(request, revision_id):
    revision = Revision.objects.get(pk=revision_id)
    response = HttpResponse(revision.file)
    type, encoding = mimetypes.guess_type(revision.file.name)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = revision.file_size
    response['Content-Disposition'] = 'attachment; filename="%s"' % (revision.file.name.split('/')[-1])
    
    return response
