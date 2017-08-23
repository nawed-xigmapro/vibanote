from django.db import models
from django.utils import timezone

class ContactInfo(models.Model):
    email = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    
  
