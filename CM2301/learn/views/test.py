from django.shortcuts import render
from learn.forms import *
from learn.models import Lecture, Module, Link
from django.contrib.auth.decorators import login_required

@login_required
def test(request, test_id):
	values = {}
	values['test'] = Test.objects.get(pk=test_id)
	values['lectures'] = values['test'].lecture.module.lecture_set.all()
	values['questions'] = values['test'].questions.all()

	#Don't quite understand this, have hashed something that looks right, needs checking though
	values['breadcrumb'] = ("LCARS", "%s (%s)"%(values['test'].title,values['test'].description))

	return render(request, 'test.html', values)

