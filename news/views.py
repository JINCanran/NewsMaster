#news view
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from news.models import *
from news.spiderformainlist import *
from django.template import RequestContext
from django.core.paginator import Paginator


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
	if 'query' in request.GET and request.GET['query']:
		query = request.GET['query']
		cur_page = int(request.GET['cur_page'])
		req_page = int(request.GET['req_page'])
		if req_page < -1 :
			req_page = cur_page+1
		elif req_page < 0 :
			req_page = cur_page-1
		if cur_page == 0 :
			spider = GetNewsList(query,3)
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
		news_list2 = MainNewsList.objects.all()
		page = Paginator(news_list2, 5)		
		news_page_list = page.page(req_page).object_list
		page_range = page.page_range
		num_pages = page.num_pages
		return render_to_response('result.html',
		{'news_list' : news_page_list,'query': query,'page_range' : page_range,'num_pages' : num_pages,'cur_page' : req_page})						
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
	
	