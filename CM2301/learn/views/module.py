from django.shortcuts import render
from learn.models import Module, Lecture, Attachment

def module(request, module_id):
    values = {}
    values['module'] =  Module.objects.get(pk=module_id)
    values['modules'] = Module.objects.all()
    values['title'] = "Module %s"%(values['module'].title)
    values['lectures'] = Lecture.objects.filter(module=module_id)
    values['attachments'] = Attachment.objects.filter(object_id=module_id)
    return render(request, 'module_detail.html', values) 


def modules(request):
    values = {}
    values['title'] =  "Module Overview"
    values['modules'] = Module.objects.all()

    return render(request, 'modules_overview.html', values)

