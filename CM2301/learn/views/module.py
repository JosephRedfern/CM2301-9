from django.shortcuts import render
from learn.models import Module, Lecture

def module(request, module_id):
    values = {}
    values['title'] = "Module"
    values['module'] =  Module.objects.get(pk=module_id)
    values['modules'] = Module.objects.all()
    values['lectures'] = Lecture.objects.all()
    return render(request, 'module_detail.html', values) 


def modules(request):
    values = {}
    values['title'] =  "Module Overview"
    values['modules'] = Module.objects.all()

    return render(request, 'modules_overview.html', values)
