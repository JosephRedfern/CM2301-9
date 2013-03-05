from django.shortcuts import render
from learn.models import Module, Lecture, Attachment, Link
from django.contrib.auth.decorators import login_required

@login_required
def module(request, module_id):
    values = {}
    values['module'] =  Module.objects.get(pk=module_id)
    values['modules'] = Module.objects.all()
    values['title'] = "Module %s"%(values['module'].title)
    values['lectures'] = Lecture.objects.filter(module=module_id)
    values['attachments'] = Attachment.objects.filter(object_id=module_id)
    values['links'] = Link.objects.filter(object_id=module_id)
    values['breadcrumb'] = ("LCARS", "%s (%s)"%(values['module'].title,values['module'].module_code))
    return render(request, 'module_detail.html', values) 

@login_required
def modules(request):
    values = {}
    values['title'] =  "Module Overview"
    values['modules'] = Module.objects.all()
    values['breadcrumb'] = ("LCARS","Module Overview")
    return render(request, 'modules_overview.html', values)


@login_required
def lectures(request, module_id):
    values = {}
    values['title'] = "Lecture Overview"
    values['lectures'] = Lecture.objects.filter(module=module_id)
    values['module'] = Module.objects.get(pk=module_id)
    values['modules'] = Module.objects.all()
    values['breadcrumb'] = ("LCARS", "%s (%s)" % (values['module'].title, values['module'].module_code), "Lectures")
    return render(request, 'lectures.html', values)

@login_required
def attachments(request, module_id):
    values = {}
    values['attachments'] = Attachment.objects.filter(object_id=module_id)
    values['modules'] = Module.objects.all()
    values['module'] = Module.objects.get(pk=module_id)
    values['lectures'] = Lecture.objects.filter(module=module_id)
    values['breadcrumb'] = ("LCARS", values['module'].title, "Attachments")

    return render(request, 'module_attachments.html', values)