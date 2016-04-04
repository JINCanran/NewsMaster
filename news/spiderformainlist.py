#__author__ = 'JCR'
from urllib import request,parse,error
from bs4 import BeautifulSoup
import http.cookiejar
import http.cookies
import re
import os
#from news.models import *

#http://world.huanqiu.com/regions/2.html

#search news for some keywords in title

class GetNewsList:
	#initial for special keyword and search range of pages
	def __init__(self,keyword,rangeNum):
		self.keyword = keyword
		self.rangeNum = rangeNum
	#get the list page include title,url,image,date
	def getListPage(self,pageNumber):
		if pageNumber == 1:
			pageNumber = 'index'
		self.listurl = 'http://world.huanqiu.com/regions/'+str(pageNumber)+'.html'
		try:
			#print (self.listurl)
			req = request.Request(self.listurl)
			response = request.urlopen(req)
			return response.read()
		except error.URLError as e:
			if hasattr(e,'reason'):
				print ('connecting error for: %s'% e.reason)
				return None
	#do with the listpage to select news and save the url by saveUrl function
	def selectTitle(self):
		pattern = '.*'+self.keyword+'.*'
		contents_list = []
		for pageNumber in range(self.rangeNum):
			listsoup = BeautifulSoup(self.getListPage(pageNumber+1),'html.parser')
			tag_li = listsoup.find_all("li",class_="item")				
			for tag in tag_li:
				if re.match(pattern, tag.h3.a['title']):
					# print(tag.a['title'])
					# print(tag.a['href'])
					# if(len(tag.a.contents) > 1):
						# print(tag.a.img['src'])
					# print(tag.h5.contents[0])
					# print(tag.h6.contents[1])		
					contents ={}				
					contents['url'] = tag.a['href']				
					contents['title'] = tag.a['title']
					if(tag.a.find('img') != None):			
						contents['mediaurl'] = tag.a.img['src']
					contents['abstract'] = tag.h5.contents[0]
					contents['date'] = tag.h6.contents[1]
					contents_list.append(contents)
		return contents_list

