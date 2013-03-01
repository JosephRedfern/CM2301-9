from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from learn.models import Attachment, Revision
from learn.forms import *


def attachment(request, attachment_id):
    print attachment_id
    attachment = Attachment.objects.get(id=attachment_id)
    return render(request, 'attachment.html', {'attachment': attachment})

@require_http_methods(["GET"])
@login_required
def revision_delete(request, revision_id):
    revision = Revision.objects.get(pk=revision_id)
    if len(revision.attachment.revision_set.all()) < 2:
        return redirect(revision.attachment.get_absolute_url())
    
    revision.delete()
    return redirect(revision.attachment.get_absolute_url())
    
def revision(request, revision_id):
    revision = Revision.objects.get(pk=revision_id)
    revision.delete()