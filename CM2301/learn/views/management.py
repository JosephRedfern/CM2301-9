from django.shortcuts import render, redirect
from learn.models import *
from django.contrib.auth.views import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from learn.forms import *
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.contrib.auth.hashers import make_password


def overview(request):
    values = dict()
    values['management'] = True
    values['title'] = "Management"
    values['modules'] = []

    courses = request.user.course.all()

    for course in courses:
        [values['modules'].append(module) for module in course.modules.all()]

    values['modules'] = set(values['modules'])

    return render(request, "management_overview.html", values)


def unassociate_module(request, course_id, module_id):
    course = Course.objects.get(pk=course_id)
    module = Module.objects.get(pk=module_id)

    module.courses.remove(course)

    messages.add_message(request, messages.INFO, 'Module un-associated succesfully.')
    return redirect('/management/courses/'+course_id+'/details')

def associate_module(request, course_id):
    values = dict()

    if request.method == 'POST':
        form = ModuleAssociateForm(data=request.POST)

        if form.is_valid():
            module = form.cleaned_data['modules']
            course = Course.objects.get(pk=course_id)
            if course in module.courses.all():
                messages.add_message(request, messages.INFO, 'Module already associated.')
            else:
                module.courses.add(course)  
                module.save()
                messages.add_message(request, messages.INFO, 'Module succesfully associated')
        else:
            messages.add_message(request, messages.INFO, 'Invalid module specified')

        return redirect('/management/courses/'+course_id+'/details')

    else:
        form = ModuleAssociateForm()
        course = Course.objects.get(pk=course_id)
        current_modules = course.modules.all()
        form.fields['modules'].queryset = Module.objects.all().exclude(pk__in = current_modules)
        values['course_id'] = course_id
        values['form'] = form
        return render(request, "management_course_associate.html", values)



class UserListView(ListView):
    model = User
    template_name = "management_users.html"

    def get_context_data(self, **kwargs):
            context = super(UserListView, self).get_context_data(**kwargs)
            context['management'] = True
            context['title'] = "User Management"
            context['modules'] = []

            courses = self.request.user.course.all()

            for course in courses:
                [context['modules'].append(module) for module in course.modules.all()]

            context['modules'] = set(context['modules'])
            return context


class UserUpdateView(UpdateView):
    model = User
    template_name = "management_user_update.html"
    success_url= "/management/users"

    def get_context_data(self, **kwargs):
            context = super(UserUpdateView, self).get_context_data(**kwargs)
            context['management'] = True
            context['pk'] = self.kwargs['pk']
            context['modules'] = []

            courses = self.request.user.course.all()

            for course in courses:
                [context['modules'].append(module) for module in course.modules.all()]

            context['modules'] = set(context['modules'])
            return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        return super(UserUpdateView, self).form_valid(form)

class UserCreateView(CreateView):
    model = User
    template_name = "management_user_create.html"
    success_url= "/management/users"

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['modules'] = []

        courses = self.request.user.course.all()

        for course in courses:
            [context['modules'].append(module) for module in course.modules.all()]

        context['modules'] = set(context['modules'])

        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        return super(UserCreateView, self).form_valid(form)

class CourseListView(ListView):
    model = Course
    template_name = "management_courses.html"

    def get_context_data(self, **kwargs):
            context = super(CourseListView, self).get_context_data(**kwargs)
            context['management'] = True
            context['title'] = "Course Management"
            context['modules'] = []

            courses = self.request.user.course.all()

            for course in courses:
                [context['modules'].append(module) for module in course.modules.all()]

            context['modules'] = set(context['modules'])

            return context

class CourseUpdateView(UpdateView):
    model = Course
    template_name = "management_course_update.html"
    success_url= "/management/courses"

    def get_context_data(self, **kwargs):
            context = super(CourseUpdateView, self).get_context_data(**kwargs)
            context['management'] = True
            context['pk'] = self.kwargs['pk']

            context['modules'] = []

            courses = self.request.user.course.all()

            for course in courses:
                [context['modules'].append(module) for module in course.modules.all()]

            context['modules'] = set(context['modules'])
            return context

class CourseDetailView(DetailView):
    model = Course
    template_name = "management_course_detail.html"

    def get_context_data(self, **kwargs):
            context = super(CourseDetailView, self).get_context_data(**kwargs)
            context['management'] = True
            context['title'] = "Course Details"
            context['modules'] = []

            courses = self.request.user.course.all()

            for course in courses:
                [context['modules'].append(module) for module in course.modules.all()]

            context['modules'] = set(context['modules'])
            return context

class CourseCreateView(CreateView):
    model = Course
    template_name = "management_course_create.html"
    success_url = "/management/courses"

    def get_context_data(self, **kwargs):
        context = super(CourseCreateView, self).get_context_data(**kwargs)
        context['modules'] = []

        courses = self.request.user.course.all()

        for course in courses:
            [context['modules'].append(module) for module in course.modules.all()]

        context['modules'] = set(context['modules'])

        return context


class ModuleListView(ListView):
    model = Module
    template_name = "management_modules.html"

    def get_context_data(self, **kwargs):
        context = super(ModuleListView, self).get_context_data(**kwargs)
        context['management'] = True
        context['modules'] = []

        courses = self.request.user.course.all()

        for course in courses:
            [context['modules'].append(module) for module in course.modules.all()]

        context['modules'] = set(context['modules'])

        return context

class ModuleDeleteView(DeleteView):
    model = Module
    template_name = "management_module_delete.html"
    success_url = "/management/modules"

class LectureListView(ListView):
    model = Lecture
    template_name = "management_module_lectures.html"

    def get_context_data(self, **kwargs):
        context = super(LectureListView, self).get_context_data(**kwargs)
        context['management'] = True
        context['modules'] = []

        courses = self.request.user.course.all()

        for course in courses:
            [context['modules'].append(module) for module in course.modules.all()]

        context['modules'] = set(context['modules'])

        print context

        return context

class ManagementCourseworkTaskListView(ListView):
    model = CourseworkTask
    template_name = "management_coursework_tasks.html"

    def get_context_data(self, **kwargs):
        context = super(ManagementCourseworkTaskListView, self).get_context_data(**kwargs)
        context['management'] = True
        context['title'] = "Coursework Task List"
        context['courseworktask_list'] = CourseworkTask.objects.filter(module=self.kwargs['pk'])
        print dir(self)

        return context


@staff_member_required
def mark_coursework(request, module_id, task_id, submission_id):
    if request.method == "POST":
        form = MarkCourseworkForm(data=request.POST)

        if form.is_valid():
            score = form.cleaned_data['score']
            submission = CourseworkSubmission.objects.get(pk=submission_id)
            submission.score = score
            submission.save()
            messages.add_message(request, messages.INFO, 'Coursework marked')

        else:
            messages.add_message(request, messages.INFO, 'Invalid mark specified')

        return redirect("/management/modules/"+str(module_id)+"/coursework/"+str(task_id))

    else:
        form = MarkCourseworkForm()
        values = {}
        values['form'] = form
        values['module_id'] = module_id
        values['task_id'] = task_id
        values['submission_id'] = submission_id
        values['current_mark'] = CourseworkSubmission.objects.get(pk=submission_id).score

        return render(request, "management_coursework_mark.html", values)


class ManagementCourseworkSubmissionListView(ListView):
    model = CourseworkSubmission
    template_name = "management_coursework_submissions.html"

    def get_context_data(self, **kwargs):
        context = super(ManagementCourseworkSubmissionListView, self).get_context_data(**kwargs)
        context['management'] = True
        context['title'] = "Coursework Submissions"
        context['courseworksubmission_list'] = CourseworkSubmission.objects.filter(coursework_task=CourseworkTask.objects.get(pk=self.kwargs['pk']))
        print dir(self)

        return context

