#news view
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from news.models import *
from news.spiderformainlist import *
from django.template import RequestContext

# Create your views here.
def index(request):
	username = request.COOKIES.get('username','')
	return render_to_response('index.html',{'username': username}
	,context_instance=RequestContext(request))

def logout(request):
	response = HttpResponseRedirect('/index/')
	response.delete_cookie('username')
	return response

	
def result(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		spider = GetNewsList(q,2)
		news_list = spider.selectTitle()
		MainNewsList.objects.all().delete()
		for news in news_list:
			news1 = MainNewsList(title = news['title'],
			url = news['url'],
			abstract = news['abstract'],
			mediaurl = news.get('mediaurl'),
			date = news['date']
			)	
			news1.save()
		return render_to_response('result.html',
		{'news_list': news_list,'query': q})						
	else:
		return HttpResponse('Please submit a search term.')
		
def register(request):
	errors = []
	if request.method == 'POST':
		if not request.POST.get('username', ''):
			errors.append('Enter a username.')
		if not request.POST.get('password', ''):
			errors.append('Enter a password.')
		if not (request.POST.get('password', '') ==request.POST.get('password2', '')):
			errors.append('Password not same')
		if not errors:
			username = request.POST.get('username', '')
			users = User.objects.filter(name = username)
			if not (len(users) == 0):
				errors.append('Username used!')
				return render_to_response('register.html',{'errors': errors,'email':request.POST.get('email',''),'message':request.POST.get('message','')}
				,context_instance=RequestContext(request))
			user1 = User(name = request.POST.get('username', ''),
			password = request.POST.get('password', ''),
			)
			user1.save()
			return render_to_response('login.html',{'username':request.POST.get("username",''),},context_instance=RequestContext(request))
	return render_to_response('register.html',{'errors': errors,'username':request.POST.get("username",''),'password':request.POST.get('password',''),
	'password2':request.POST.get('password2',''),'email':request.POST.get('email',''),'message':request.POST.get('message','')}
	,context_instance=RequestContext(request))
	
def login(request):
	errors = []
	if request.method == 'POST':
		if not request.POST.get('username', ''):
			errors.append('Enter a username.')
		if not request.POST.get('password', ''):
			errors.append('Enter a password.')
		if not errors:
			username = request.POST.get('username', '')
			pwd = request.POST.get('password', '')
			users = User.objects.filter(name = username,password = pwd)
			if (len(users) == 0):
				errors.append('User not existed!')
				return render_to_response('login.html',{'errors': errors}
				,context_instance=RequestContext(request))
			else :
				response = HttpResponseRedirect('/index/')
				response.set_cookie('username',username,3600)
				return response
	return render_to_response('login.html',{'errors': errors}
	,context_instance=RequestContext(request))
	
	