from django.shortcuts import render, redirect
from learn.models import *
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from learn.forms import *
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.hashers import make_password


def overview(request):
    values = dict()
    values['management'] = True
    return render(request, "management_overview.html", values)


class UserListView(ListView):
    model = User
    template_name = "management_users.html"

    def get_context_data(self, **kwargs):
            context = super(UserListView, self).get_context_data(**kwargs)
            context['management'] = True
            return context


class UserUpdateView(UpdateView):
    model = User
    template_name = "management_user_update.html"
    success_url= "/management/users"

    def get_context_data(self, **kwargs):
            context = super(UserUpdateView, self).get_context_data(**kwargs)
            context['management'] = True
            context['pk'] = self.kwargs['pk']
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
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        return super(UserUpdateView, self).form_valid(form)

class CourseListView(ListView):
    model = Course
    template_name = "management_courses.html"

    def get_context_data(self, **kwargs):
            context = super(CourseListView, self).get_context_data(**kwargs)
            context['management'] = True
            return context

class CourseUpdateView(UpdateView):
    model = Course
    template_name = "management_course_update.html"
    success_url= "/management/courses"

    def get_context_data(self, **kwargs):
            context = super(CourseUpdateView, self).get_context_data(**kwargs)
            context['management'] = True
            context['pk'] = self.kwargs['pk']
            return context

class CourseCreateView(CreateView):
    model = Course
    template_name = "management_course_create.html"
    success_url = "/management/courses"

    def get_context_data(self, **kwargs):
        context = super(CourseCreateView, self).get_context_data(**kwargs)
        return context