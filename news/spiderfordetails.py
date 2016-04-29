#__author__ = 'JCR'
from urllib import request,parse,error
from bs4 import BeautifulSoup
import http.cookiejar
import http.cookies
import re
import os

#from news.models import *


#nersion 1 just for huanqiu page
class GetNewsDetails:
	#initial for special keyword and search range of pages
	def __init__(self,url):
		self.url = url
	
	#get the required page include title,url,mediaurl,date,source,text
	def getPage(self):
		try:
			req = request.Request(self.url)
			response = request.urlopen(req)
			return response.read()
		except error.URLError as e:
			if hasattr(e,'reason'):
				print ('connecting error for: %s'% e.reason)
				return None
	#解析获取网页信息
	def getInfo(self):
		soup = BeautifulSoup(self.getPage(),'lxml')		
		contents = {}
		fromtag = soup.find('strong',class_="fromSummary").a
		title = soup.find('div',class_="conText").h1.string
		date = soup.find('strong',class_="timeSummary").string
		source = fromtag.string
		url = fromtag['href']
		tagp = soup.find('div',class_="text").find_all('p')
		text = ''
		for p in tagp:
			text += str(p)		
		contents['title'] = title
		contents['date'] = date
		contents['source'] = source
		contents['url'] = url
		contents['text'] = text
		return(contents)	

