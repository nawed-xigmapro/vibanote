from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateTimeField(default=datetime.now,null=True,blank=True)
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
    reason = models.TextField(null=True)
    activateit = models.IntegerField(null=True,blank=True)
    forgotstr = models.CharField(max_length=200,null=True)
    
class Cms(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200,null=True)
    text = models.TextField(null=True)
    slug = models.CharField(max_length=200,null=True)
    created_date = models.DateTimeField(
            default=timezone.now)     
