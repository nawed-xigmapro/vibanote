from django.db import models
from django.utils import timezone

class NewsLetter(models.Model):
    email = models.CharField(max_length=100,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    
  
