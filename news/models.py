from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    User = models.ForeignKey(User)
    publication_date = models.DateField()
	
class News(models.Model):
	title = models.CharField(max_length=100)
	data = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	text = models.CharField(max_length=1000)
    