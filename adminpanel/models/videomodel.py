from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from adminpanel.models.typemodel import *
from adminpanel.models.genremodel import *

class Video(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    slug = models.CharField(max_length=100,null=True,blank=True)
    subtitle = models.CharField(max_length=200,null=True,blank=True)
    link = models.CharField(max_length=255,null=True,blank=True)
    link_url = models.CharField(max_length=255,null=True,blank=True)
    dedicate = models.CharField(max_length=255,null=True,blank=True)
    is_approved = models.IntegerField(null=True,blank=True)
    like_counts = models.IntegerField(null=True,blank=True)
    genre=models.ForeignKey(Genre, on_delete=models.CASCADE,null=True,blank=True)
    types=models.ForeignKey(Type, on_delete=models.CASCADE,null=True,blank=True)
    uploadby = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    
  
