from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from learn.models import Attachment, Revision
from learn.forms import *


def attachment(request, attachment_id):
    attachment = Attachment.objects.get(pk=attachment_id)
    return render(request, 'attachment.html', {'attachment': attachment})

@require_http_methods(["GET"])
@login_required
def revision_delete(request, revision_id):
    revision = Revision.objects.get(pk=revision_id)
    revision.delete()
    return HttpResponse('Deleted')
    
def revision(request, revision_id):
    revision = Revision.objects.get(pk=revision_id)
    revision.delete()