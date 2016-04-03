#news view
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from news.models import *
from news.spiderforonepage import *
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

	
def search_result(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		spiderForPage = SearchNews(q,1)
		spiderForPage.saveUrl()
		with open(q + ".txt", "r")  as f: 
			for line in filter(None,f):
				spiderForNews = SpiderForWorldNews(line)
				spiderForNews.getInfo()
			news = News.objects.filter(title__icontains=q)
			return render_to_response('search_result.html',
			{'news': news,'query': q})		
				
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
	
	