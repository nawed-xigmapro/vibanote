from django.db import models
from django.utils import timezone

class Type(models.Model):
    title = models.CharField(max_length=100,null=True)
    text = models.CharField(max_length=200,null=True)
    slug = models.CharField(max_length=100,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    
  
