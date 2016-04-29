#news view
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from news.models import *
from news.spiderformainlist import *
from news.spiderfordetails import *
from django.template import RequestContext
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.contrib import auth
import time;
import sys   
sys.setrecursionlimit(1000000)

# Create your views here.
def index(request):
	username = request.COOKIES.get('username','')
	keys = UserToKey.objects.filter(username = username)
	if 'cur_page' in request.GET and request.GET['cur_page']:
		cur_page = int(request.GET['cur_page'])
	else:
		cur_page = 0
	if 'req_page' in request.GET and request.GET['req_page']:
		req_page = int(request.GET['req_page'])
	else:
		req_page = 1	
	if req_page < -1 :
		req_page = cur_page+1
	elif req_page < 0 :
		req_page = cur_page-1		
	if 'query' in request.GET and request.GET['query']:
		query = request.GET['query']
		#由cur_page区分是否翻页，翻页请求不需重复爬取
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
		news_list2 = MainNewsList.objects.order_by("-date")[0:100]
	else :
		query = None
		#由cur_page区分是否翻页，翻页请求不需重复爬取
		if cur_page == 0 :	
			MainNewsList.objects.all().delete()			
			for key in keys:			
				spider = GetNewsList(key.key,2)
				news_list = spider.selectTitle()
				for news in news_list:
					news1 = MainNewsList(title = news['title'],
					url = news['url'],
					abstract = news['abstract'],
					mediaurl = news.get('mediaurl'),
					date = news['date']
					)	
					news1.save()		
		news_list2 = MainNewsList.objects.order_by("-date")[0:100]
	
	if cache.get('chinalist') == None:
		spiderforchina = GetNewsList("",1,'http://china.huanqiu.com/local/')
		chinalist = spiderforchina.selectTitle()[0:5]
		cache.set('chinalist',chinalist)
	else :
		chinalist = cache.get('chinalist')
	if cache.get('worldlist') == None:
		spiderforworld = GetNewsList("",1)	
		worldlist = spiderforworld.selectTitle()[0:5]
		cache.set('worldlist',worldlist)
	else :
		worldlist = cache.get('worldlist')

	
	
	
	page = Paginator(news_list2, 5)		
	news_page_list = page.page(req_page).object_list
	page_range = page.page_range
	num_pages = page.num_pages
	return render_to_response('index.html',
	{'username': username,'news_list' : news_page_list,'query': query,
	'page_range' : page_range,'num_pages' : num_pages,'cur_page' : req_page,'keys':keys,'chinalist':chinalist,'worldlist':worldlist})	

def logout(request):
	response = HttpResponseRedirect('/index/')
	response.delete_cookie('username')
	return response
	
@cache_page(60 * 15)
def details(request):
	username = request.COOKIES.get('username','')
	if 'cur_page' in request.GET and request.GET['cur_page']:
		cur_page = int(request.GET['cur_page'])
	
		req_page = int(request.GET['req_page'])
	if 'title' in request.GET and request.GET['title']:
		title = request.GET['title']
	if 'url' in request.GET and request.GET['url']:
		url = request.GET['url']				
	if req_page < -1 :
		req_page = cur_page+1
	elif req_page < 0 :
		req_page = cur_page-1
	#由cur_page区分是否翻页，翻页请求不需重复爬取
	if cur_page == 0 :	
		NewsDetails.objects.all().delete()
		spider = GetNewsDetails(url)
		contents = spider.getInfo()
		details = NewsDetails(title = contents['title'],
				url = contents['url'],
				text = contents['text'],
				date = contents['date'],
				source = contents['source']
				)	
		details.save()
		title = contents['title']
	if 'message' in request.GET and request.GET['message']:
		message = request.GET['message']
		comment = Comment(username = username,
		title = title,message = message,date = time.asctime( time.localtime(time.time()) ))
		comment.save()
	contents = NewsDetails.objects.all()[0]
	page = Paginator(Comment.objects.filter(title = title), 5)		
	comment_list = page.page(req_page).object_list
	page_range = page.page_range
	num_pages = page.num_pages	
	return render_to_response('details.html',{'username': username,'contents':contents,'comment_list':comment_list,
	'page_range' : page_range,'num_pages' : num_pages,'cur_page' : req_page}
	,context_instance=RequestContext(request))
	
@cache_page(60 * 15)	
def result(request):
	username = request.COOKIES.get('username','')
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
		news_list2 = MainNewsList.objects.all()[0:100]
		#使用Paginator工具进行分页
		page = Paginator(news_list2, 5)		
		news_page_list = page.page(req_page).object_list
		page_range = page.page_range
		num_pages = page.num_pages
		return render_to_response('result.html',
		{'username': username,'news_list' : news_page_list,'query': query,
		'page_range' : page_range,'num_pages' : num_pages,'cur_page' : req_page})						
	else:
		return HttpResponse('Please submit a search term.')
		
def register(request):
	errors = []
	if request.method == 'POST':
		#验证输入规范
		if not request.POST.get('username', ''):
			errors.append('Enter a username.')
		if not request.POST.get('password', ''):
			errors.append('Enter a password.')
		if not (request.POST.get('password', '') ==request.POST.get('password2', '')):
			errors.append('Password not same')
		if not errors:
			username = request.POST.get('username', '')
			users = User.objects.filter(username = username)
			if not (len(users) == 0):
				errors.append('Username used!')
				return render_to_response('register.html',{'errors': errors,'email':request.POST.get('email',''),'message':request.POST.get('message','')}
				,context_instance=RequestContext(request))
			user1 = User(username = request.POST.get('username', ''),
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
        # Check that the test cookie worked (we set it below):
		#if request.session.test_cookie_worked():
		if True:
            # The test cookie worked, so delete it.
			#request.session.delete_test_cookie()

            # In practice, we'd need some logic to check username/password
			if not request.POST.get('username', ''):
				errors.append('Enter a username.')
			if not request.POST.get('password', ''):
				errors.append('Enter a password.')
			if not errors:
				username = request.POST.get('username', '')
				pwd = request.POST.get('password', '')
				users = User.objects.filter(username = username,password = pwd)
				if (len(users) == 0):
					errors.append('User not existed!')
					return render_to_response('login.html',{'errors': errors}
					,context_instance=RequestContext(request))
				else :
					response = HttpResponseRedirect('/index/')
					response.set_cookie('username',username,3600)
					return response
           

        # The test cookie failed, so display an error message. If this
        # were a real site, we'd want to display a friendlier message.
		else:
			#request.session.set_test_cookie()
			return HttpResponse("Please enable cookies and try again.")

    # If we didn't post, send the test cookie along with the login form.
	
	return render_to_response('login.html',{'errors': errors}
					,context_instance=RequestContext(request))
					
def addkey(request):
	errors = []
	username = request.COOKIES.get('username','')
	uks = UserToKey.objects.filter(username = username)
	if request.method == 'POST':
		if not request.POST.get('key', ''):
			errors.append('Enter a keyword.')
		if not errors:
			key = request.POST.get('key', '')
			#if len(uks = UserToKey.objects.filter(username = username,key = key)) > 0:
			#	errors.append('您已添加此关键字')
			#else :
			uk = UserToKey(username = username,key = key)
			uk.save()
			errors.append('add a keyword....ok!')
			return render_to_response('addkey.html',{'errors':errors,'username':username,'uks':uks},context_instance=RequestContext(request))
	return render_to_response('addkey.html',{'errors':errors,'username':username,'uks':uks},context_instance=RequestContext(request))
	
	