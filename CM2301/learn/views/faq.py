from django.shortcuts import render
from learn.models import *
from django.contrib.auth.decorators import login_required

@login_required
def faqs(request, module_id):
    values = dict()
    values['module'] = Module.objects.get(pk=module_id)
    values['lectures'] = values['module'].lecture_set.all
    values['faqs'] = FAQQuestion.objects.filter(module=values['module'])
    return render(request, 'faqs.html', values)
