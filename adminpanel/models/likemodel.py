from django.db import models
from django.utils import timezone
from adminpanel.models.videomodel import *
from adminpanel.models.albummodel import *
from adminpanel.models.trackmodel import *

class Likes(models.Model):
    like_type = models.CharField(max_length=100,null=True)
    video=models.ForeignKey(Video, on_delete=models.CASCADE,null=True,blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE,null=True,blank=True)
    track = models.ForeignKey(Tracks, on_delete=models.CASCADE,null=True,blank=True)
    artist = models.ForeignKey(User, related_name='artist_likes', on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User,related_name='user_likes', on_delete=models.CASCADE,null=True,blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    
  
