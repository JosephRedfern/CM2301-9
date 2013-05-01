from django.shortcuts import render, redirect
from learn.models import *
from learn.forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView
from django.core.exceptions import ObjectDoesNotExist


class CourseworkListView(ListView):
    model = CourseworkTask
    template_name = "module_coursework.html"

    def get_context_data(self, **kwargs):
        module = Module.objects.get(pk=self.kwargs['pk'])
        context = super(CourseworkListView, self).get_context_data(**kwargs)
        context['coursework_list'] = CourseworkTask.objects.filter(module=module)
        context['modules'] = []
        context['module'] = module

        courses = self.request.user.course.all()

        for course in courses:
            [context['modules'].append(module) for module in course.modules.all()]

        context['modules'] = set(context['modules'])

        courseworktasks = CourseworkTask.objects.filter(module=module)

        context['tasks_with_results'] = []
        for task in courseworktasks:
            try:
                context['tasks_with_results'].append({'task': task, 'score':task.courseworksubmission_set.get(student=self.request.user).score})
            except ObjectDoesNotExist:
                context['tasks_with_results'].append({'task': task})


        return context


class CourseworkTaskCreateView(CreateView):
    model = CourseworkTask
    template_name = "module_coursework_create.html"

    def get_context_data(self, **kwargs):
       context = super(CourseworkTaskCreateView, self).get_context_data(**kwargs)
       context['module_id'] = self.kwargs['pk']
       return context

    def form_valid(self, form):
        task = form.save(commit=False)
        task.module = Module.objects.get(pk=self.kwargs['pk'])
        task.save()
        return super(CourseworkTaskCreateView, self).form_valid(form)

@login_required
def coursework_submission(request, module_id, coursework_id):
    values = dict()

    if request.method == 'POST':
        form = CourseworkSubmissionForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            submission = CourseworkSubmission()
            submission.student = request.user
            submission.attachments = form.cleaned_data['submission']
            submission.coursework_task = CourseworkTask.objects.get(pk=coursework_id)
            submission.score = -1
            submission.save()
            messages.add_message(request, messages.INFO, 'Coursework Uploaded!')
        else:
            messages.add_message(request, messages.INFO, 'Upload Failed - did you choose a valid file?')
        return redirect('/modules/'+module_id+"/coursework")
    else:
        values['form'] = CourseworkSubmissionForm()
        values['module_id'] = module_id
        values['coursework_id'] = coursework_id
        return render(request, "module_coursework_submit.html", values)
