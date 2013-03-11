from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from learn.models import Attachment, Revision, Module, Lecture
from django.core import serializers
from learn.forms import *
import mimetypes, tempfile, zipfile

@login_required 
def attachment(request, attachment_id):
    Viewed.log_view(request, attachment_id)
    values = {}
    values['attachment'] = Attachment.objects.get(id=attachment_id)
    values['title'] = "Attachment %s"%(values['attachment'].file_name)
    values['modules'] = Module.objects.all()
    try:
        values['lectures'] = Lecture.objects.get(id=values['attachment'].object_id).module.lecture_set.all()
    except:
        pass

    values['breadcrumb'] = ("LCARS", "Attachments")
    
    form = RevisionForm(initial={'attachment': attachment_id, 'uploaded_by': request.user})
    values['form'] = form
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

@login_required  
def revision(request, revision_id):
    revision = Revision.objects.get(pk=revision_id)
    revision.delete()

@login_required 
def revision_download(request, revision_id):
    Viewed.log_view(request, revision_id)
    revision = Revision.objects.get(pk=revision_id)
    response = HttpResponse(revision.file)
    type = revision.mimetype()
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = revision.file_size
    response['Content-Disposition'] = 'attachment; filename="%s"' % (revision.file.name.split('/')[-1])
    
    return response

@login_required 
def revision_add(request, attachment_id):
    if request.method == 'POST':
        form = RevisionForm(request.POST, request.FILES)
        if form.is_valid():
            revision = form.save()
            #return redirect(revision.attachment.get_absolute_url())
            revisions = Revision.objects.filter(pk=revision.id)
            data = serializers.serialize('json', revisions)
            return HttpResponse(data)
    attachment = Attachment.objects.get(pk=attachment_id)
    form = RevisionForm(initial={'attachment': attachment, 'uploaded_by': request.user})
    return render(request, 'revision.html', {'form': form})
    
        

@login_required 
def download_all_revisions(request, attachment_id):
    """
    Sends a zip file of all revisions associated with the current 
    attachment to the client. Prefixing filenames with the relevent 
    version number.
    
    """
    attachment = Attachment.objects.get(pk=attachment_id)
    f = attachment.compress_revisions(method='zip')
    response = HttpResponse(f)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="%s.zip"' % (attachment.id)
    return response

@login_required
def download_all_attachments(request, object_id):
    attachments = Attachment.objects.filter(object_id=object_id)
    tmp = tempfile.NamedTemporaryFile(delete=False)
    z = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
    for attachment in attachments:
        print attachment.get_latest_revision().file.file.name
        z.write(attachment.get_latest_revision().file.file.name, attachment.file_name)
    z.close()
    tmp.seek(0)
    response = HttpResponse(tmp)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="%s.zip"' % (attachment.id)
    return response
    
@login_required
def attachment_create(request, object_id):
    if request.method == 'POST':
        attachment = AttachmentForm(request.POST, prefix='attachment').save(commit=False)
        revision = RevisionForm(request.POST, request.FILES, prefix='revision').save(commit=False)
        attachment.owner = request.user
        attachment.save()
        revision.attachment = attachment
        revision.uploaded_by = request.user
        revision.save()
        return redirect(attachment.get_absolute_url())
        
    attachment_form = AttachmentForm(prefix='attachment', initial={'object_id': object_id})
    revision_form = RevisionForm(prefix='revision')
    return render(request, 'attachment_create.html', {'attachment_form': attachment_form, 'revision_form': revision_form})
    
