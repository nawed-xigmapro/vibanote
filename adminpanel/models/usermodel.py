from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
from adminpanel.models.genremodel import *
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    dob = models.DateTimeField(null=True,blank=True)
    gender = models.CharField(max_length=100,null=True)
    description =  models.TextField(null=True)
    picture = models.ImageField(upload_to = 'media', null=True)
    medium_pic = models.CharField(max_length=200,null=True)
    thumbnail_pic = models.CharField(max_length=200,null=True)
    isfeatured = models.IntegerField(null=True,blank=True)
    address = models.TextField(null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    country = models.CharField(max_length=200,null=True)
    website = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    phone_code = models.IntegerField(null=True,blank=True)
    reason = models.TextField(null=True)
    activateit = models.IntegerField(null=True,blank=True)
    genre=models.ForeignKey(Genre,null=True,blank=True)
    like_counts = models.IntegerField(null=True,blank=True)
    most_browsed = models.IntegerField(default=0,null=True)
    forgotstr = models.CharField(max_length=200,null=True)
    is_loggedin = models.IntegerField(null=True,blank=True,default=0)
  
