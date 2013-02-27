from django.shortcuts import render
from learn.forms import *


def login(request):
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})