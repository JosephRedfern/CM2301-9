from django.shortcuts import render, redirect
from learn.models import Video, User, Announcement
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from learn.forms import *
