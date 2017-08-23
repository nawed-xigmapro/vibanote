from django.db import models
class EmailTemplates(models.Model):    
    templatename = models.CharField(max_length=100,null=True,blank=True)
    templatebody = models.TextField(null=True,blank=True)
    subject = models.CharField(max_length=100,null=True,blank=True)