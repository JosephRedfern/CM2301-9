from django.shortcuts import render
from learn.models import *
from learn.forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView


class CreateAnnouncementView(CreateView):
    model = Announcement
    template_name = "announcement_form.html"

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.owner = self.request.user
        announcement.save()
        return super(CreateAnnouncementView, self).form_valid(form)