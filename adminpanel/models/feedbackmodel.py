from django.db import models
class Feedback(models.Model):    
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    contactno = models.CharField(max_length=100,null=True,blank=True)
    feedback_text = models.TextField(null=True,blank=True)