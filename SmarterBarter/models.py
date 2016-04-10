from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
# Create your models here.
class Book(models.Model):
	bookName=models.CharField(max_length=200)
	subject=models.CharField(max_length=100)
	semester=models.IntegerField(null=True,blank=True)
	copiesLeft=models.IntegerField(default=0)
	noOfRequests=models.IntegerField(default=0)
	currentRequests=models.CharField(max_length=500,blank=True)
	def __str__(self):
		return u'%s %d'%(self.bookName,self.id)

"""class Teacher(AbstractBaseUser):
	username=models.IntegerField(default=0)
	first_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)
	email=models.EmailField(blank=True)
	USERNAME_FIELD=('SAP')
	def __str__(self):
		return u'%s %s'%(self.first_name,self.last_name)	
	"""

"""class Student(AbstractBaseUser):
	SAP=models.IntegerField(default=0)
	first_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)
	email=models.EmailField(blank=True)
	USERNAME_FIELD=('SAP')	
	def __str__(self):
		return u'%d'%(self.SAP)
"""
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)


    # The additional attributes we wish to include.
    YEAR_CHOICE=(("First Year","fe"),("Second Year","se"),("Third Year","te"),("Fourth Year","be"))
    year=models.CharField(max_length=20,choices=YEAR_CHOICE)
    superuser=models.IntegerField(default=0)


    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return u'%s'%(self.user.username)
class ApproveRequests(models.Model):
	bookName=models.CharField(max_length=200)
	requested_by=models.CharField(max_length=100)
	issued=models.IntegerField(default=0)
	bookId=models.IntegerField()
	def __str__(self):
		return u'%s %d'%(self.requested_by,self.bookId)

class ApprovedRequests(models.Model):
	bookName=models.CharField(max_length=200)
	requested_by=models.CharField(max_length=100)
	bookId=models.IntegerField()
	def __str__(self):
		return u'%s %d'%(self.requested_by,self.bookId)




	

