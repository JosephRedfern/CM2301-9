from django.shortcuts import render
from learn.models import *
from django.contrib.auth.decorators import login_required

@login_required
def module(request, module_id):
    Viewed.log_view(request, module_id)
    values = {}
    values['module'] =  Module.objects.get(pk=module_id)
    values['modules'] = Module.objects.all()
    values['title'] = "Module %s"%(values['module'].title)
    values['lectures'] = Lecture.objects.filter(module=module_id)
    values['tests'] = Test.objects.filter(lecture__in=[x.pk for x in values['lectures']])
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


@login_required
def tests(request, module_id):
    values = {}
    values['attachments'] = Attachment.objects.filter(object_id=module_id)
    values['modules'] = Module.objects.all()
    values['module'] = Module.objects.get(pk=module_id)
    values['lectures'] = Lecture.objects.filter(module=module_id)
    values['tests'] = Test.objects.filter(lecture__in=values['lectures'])
    values['tests_with_max'] = []
    for test in values['tests']:
        test_instances = TestInstance.objects.filter(test=test).order_by('-test_score')[:1]
        if len(test_instances)>0:
            values['tests_with_max'].append((test, test_instances[0].test_score))
        else:
            values['tests_with_max'].append((test, ""))

    values['top_results'] = []
    for test in values['tests']:
        test_instances = TestInstance.objects.filter(test=test).order_by('-test_score')[:1]
        if len(test_instances)>0:
            values['top_results'].append((test, test_instances[0].test_score))

    values['bottom_results'] = []
    for test in values['tests']:
        test_instances = TestInstance.objects.filter(test=test).order_by('test_score')[:1]
        if len(test_instances)>0:
            values['bottom_results'].append((test, test_instances[0].test_score))
        
    return render(request, 'module_tests.html', values)
