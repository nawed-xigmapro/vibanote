from django.db import models
from django.utils import timezone

class Banner(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200,null=True)
    subtitle = models.CharField(max_length=200,null=True)
    text = models.TextField(null=True)
    slug = models.CharField(max_length=200,null=True)
    picture = models.ImageField(upload_to = 'media', null=True)
    is_deleted = models.IntegerField(null=True,blank=True,default=0)
    created_date = models.DateTimeField(
            default=timezone.now)     