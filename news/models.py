from django.db import models
import time;


# Create your models here.

class User(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=50)
	email = models.CharField(max_length=100,null=True)
	message = models.CharField(max_length=512,null=True)
	
	
class MainNewsList(models.Model):
	title = models.CharField(max_length=100)
	date = models.CharField(max_length=100)
	abstract = models.CharField(max_length=10000)
	url = models.CharField(max_length=1000)
	mediaurl = models.CharField(max_length=1000,null=True)
	key = models.CharField(max_length=100)
	
class DomesticNewsList(models.Model):
	title = models.CharField(max_length=100)	
	url = models.CharField(max_length=1000)
	
class InternationalNewsList(models.Model):
	title = models.CharField(max_length=100)
	url = models.CharField(max_length=1000)

    
class NewsDetails(models.Model):
	title = models.CharField(max_length=100)
	date = models.CharField(max_length=100)
	source = models.CharField(max_length=100)
	text = models.CharField(max_length=10000)
	url = models.CharField(max_length=1000)
	
class Comment(models.Model):
	username = models.CharField(max_length=30)
	title = models.CharField(max_length=100)
	message = models.CharField(max_length=512,null=True)
	date = models.CharField(max_length=100,default='Unknow')
	
class UserToKey(models.Model):
	username = models.CharField(max_length=30)
	key = models.CharField(max_length=100)