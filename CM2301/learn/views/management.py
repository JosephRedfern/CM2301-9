from django.shortcuts import render, redirect
from learn.models import *
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from learn.forms import *
from django.views.generic import CreateView, ListView, UpdateView

def overview(request):
    values=dict()
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
    template_name = "management_users_update.html"


class CourseListView(ListView):
    model = Course 
    template_name = "management_courses.html"

    def get_context_data(self, **kwargs):
            context = super(CourseListView, self).get_context_data(**kwargs)
            context['management'] = True
            return context