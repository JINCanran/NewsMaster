#__author__ = 'JCR'
from urllib import request,parse,error
from bs4 import BeautifulSoup
import http.cookiejar
import http.cookies
import re
import os
from news.models import *


#提取环球网新闻链接格式形如http://world.huanqiu.com/exclusive/2016-03/8666328.html

class SpiderForWorldNews:
	#initial for date and number in url adress
	def __init__(self,url):
		self.url = url
	#get the page
	def getPage(self):
		try:
			req = request.Request(self.url)
			response = request.urlopen(req)
			return response.read()
		except error.URLError as e:
			if hasattr(e,'reason'):
				print ('connecting error for: %s'% e.reason)
				return None
	#get the news information
	def getInfo(self):
		soup = BeautifulSoup(self.getPage(),'html.parser')
		title = soup.find('div',class_="conText").h1	
		time = soup.find('div',class_="conText").find('strong',id="pubtime_baidu")
		author = soup.find('div',class_="conText").find('span',class_="author")
		text = soup.find('div',class_="conText").find('div',id="text")
		print('标题：', end="")
		print(title.string+'\n')
		print('日期：', end="")
		print(time.string+"    ", end="")
		print('作者：', end="")
		print(author.string.strip()+'\n')
		# print('正文：', end="")
		# for string in text.stripped_strings:
			# print(string, end="")
		# print(" ")
		print('————————————————————————————————————')
		
		news1 = News(title = title.string,
					data = time.string,
					author = author.string,
					text = '')
		news1.save()

		
#search news for some key words in title
#http://world.huanqiu.com/exclusive/
#http://world.huanqiu.com/exclusive/2.html
class SearchNews:
	#initial for special keyword
	def __init__(self,keyword,rangeNum):
		self.keyword = keyword
		self.rangeNum = rangeNum
	#get the list page include title
	def getListPage(self,pageNumber):
		if pageNumber == 1:
			pageNumber = 'index'
		self.listurl = 'http://world.huanqiu.com/exclusive/'+str(pageNumber)+'.html'
		try:
			print (self.listurl)
			req = request.Request(self.listurl)
			response = request.urlopen(req)
			return response.read()
		except error.URLError as e:
			if hasattr(e,'reason'):
				print ('connecting error for: %s'% e.reason)
				return None
	#do with the listpage to select news and save the url by saveUrl function
	def selectTitle(self,pageNumber):
		pattern = '.*'+self.keyword+'.*'
		listsoup = BeautifulSoup(self.getListPage(pageNumber),'html.parser')
		titles = listsoup.find('div',class_="fallsFlow").find_all('h3')
		contents =[]
		for title in titles:
			if re.match(pattern, title.string):
				print(title.string)
				contents.append(title.a['href'])
		return contents
	
	#存找到的url
	def saveUrl(self):
		print('开始储存目标链接')
		fileName = self.keyword + ".txt"
		print('目标文件夹：'+fileName)
		f = open(fileName,"w+")
		for i in range(self.rangeNum):
			for url in self.selectTitle(i+1):
				f.write(url+"\n")
		f.close()
	
		
		
	
# spiderForPage = SearchNews('日本',3)
# spiderForPage.saveUrl()


# with open("日本.txt", "r")  as f: 
	# for line in filter(None,f):
		# spiderForNews = SpiderForWorldNews(line)
		# spiderForNews.getInfo()

# givenNumber='8666328'
# spider1 = SpiderForWorldNews(givenDate,givenNumber)
# spider1.saveUrl()
		