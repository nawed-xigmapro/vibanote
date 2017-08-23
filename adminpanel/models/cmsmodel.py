from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Cms(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200,null=True)
    text = models.TextField(null=True)
    slug = models.CharField(max_length=200,null=True)
    picture = models.ImageField(upload_to = 'media', null=True)
    created_date = models.DateTimeField(
            default=timezone.now)     
