from django.shortcuts import render, redirect
from django.http import HttpResponse
from learn.forms import TestForm
from learn.models import *
from uuidfield import UUIDField
from django.contrib.auth.decorators import login_required
from datetime import datetime



@login_required
def tests(request):
    values = {}
    values['breadcrumb'] = ["LCARS", "All Tests"]
    values['title'] = "All Tests"
    values['modules'] = Module.objects.all()
    values['tests'] = Test.objects.all()
    values['tests_with_max'] = []
    for test in values['tests']:
        test_instances = TestInstance.objects.filter(test=test).order_by('-test_score')[:1]
        if test_instances[0]:
            values['tests_with_max'].append((test, test_instances[0].test_score))
    return render(request, "tests.html", values)

@login_required
def test(request, test_id):
    Viewed.log_view(request, test_id)
    values = {}
    values['test'] = Test.objects.get(pk=test_id)
    values['lectures'] = values['test'].lecture.module.lecture_set.all()

    if request.method != 'POST':
        values['questions'] = values['test'].get_random_questions()
        request.session['questions'] = values['questions']
        values['testform'] = TestForm()
        values['testform'].initialise(questions=values['questions'])

    values['breadcrumb'] = ("LCARS", "%s (%s)"%(values['test'].title,values['test'].description))

    if request.method == 'POST':
        form = TestForm(request.POST)
        print form.data

        test_instance = TestInstance()
        test_instance.student = request.user
        test_instance.test =  values['test']
        test_instance.save()

        if form.is_valid():
            for question in request.session['questions']:
                print question.id

                if form.data[str(question.id)]:
                    print "testing"
                    result = Result()
                    result.test_instance = test_instance
                    result.question = Question.objects.get(pk=question.id)
                    result.answer = Answer.objects.get(pk=form.data[str(question.id)])
                    result.save()
                    test_instance.time_completed = datetime.now()
                    test_instance.calc_result()
                    test_instance.save()
            
            return redirect(test_instance.get_absolute_url())


    return render(request, 'test.html', values)

@login_required
def test_results(request, test_instance_id):
    Viewed.log_view(request, test_instance_id)
    values = {}
    values['lectures'] = TestInstance.objects.get(pk=test_instance_id).test.lecture.module.lecture_set.all()
    values['test_instance'] = TestInstance.objects.get(pk=test_instance_id)
    values['test'] = values['test_instance'].test

    return render(request, 'test_result.html', values)