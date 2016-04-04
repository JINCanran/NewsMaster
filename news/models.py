from django.db import models

# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=30)
	password = models.CharField(max_length=50)
	email = models.CharField(max_length=100,null=True)
	message = models.CharField(max_length=512,null=True)
	interest = models.CharField(max_length=512,null=True)
	
class MainNewsList(models.Model):
	title = models.CharField(max_length=100)
	date = models.CharField(max_length=100)
	abstract = models.CharField(max_length=10000)
	url = models.CharField(max_length=1000)
	mediaurl = models.CharField(max_length=1000,null=True)
	
class DomesticNewsList(models.Model):
	title = models.CharField(max_length=100)	
	url = models.CharField(max_length=1000)
	
class InternationalNewsList(models.Model):
	title = models.CharField(max_length=100)
	url = models.CharField(max_length=1000)

    
class NewsDetail(models.Model):
	title = models.CharField(max_length=100)
	date = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	source = models.CharField(max_length=100)
	text = models.CharField(max_length=10000)
	url = models.CharField(max_length=1000)
	mediaurl = models.CharField(max_length=1000,null=True)	