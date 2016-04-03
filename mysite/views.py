from django.http import HttpResponse
from datetime import *
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response

def hello(request):
    return HttpResponse("Hello world")
	
def current_datetime(request):
    now = datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})