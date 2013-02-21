from django.shortcuts import render
from django.http import HttpResponse
import datetime
from learn.models import module



def home(request):
    return render(request, 'base_navbar.html')

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def get_modules(request):
    
    module_list = 
    

    return modules_list

