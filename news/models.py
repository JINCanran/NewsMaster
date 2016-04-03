from django.db import models

# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=30)
	password = models.CharField(max_length=50)
	email = models.CharField(max_length=100)
	message = models.CharField(max_length=512)
	interest = models.CharField(max_length=512)
	
class News(models.Model):
	title = models.CharField(max_length=100)
	data = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	abstract = models.CharField(max_length=10000)
	link = models.CharField(max_length=1000)
    
class Detail(models.Model):
	title = models.CharField(max_length=100)
	data = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	text = models.CharField(max_length=10000)
	link = models.CharField(max_length=1000)
	mediaurl = models.CharField(max_length=1000)