from django.shortcuts import render
from django.template import context,Template,Context
from adminpanel.models import *
from frontend.contollers.commonctrl import *
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.db import connection
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_tracks_videos(request,template='frontend/explore.html'):
    videos=Video.objects.filter(is_approved=1).order_by('-like_counts').exclude(like_counts__isnull=True).exclude(like_counts=0)[:5]  
    tracks=Tracks.objects.filter(is_approved=1).order_by('-like_counts').exclude(like_counts__isnull=True).exclude(like_counts=0)[:5]
    #newest
    newest_videos=Video.objects.filter(is_approved=1).order_by('-id') 
    newest_tracks=Tracks.objects.filter(is_approved=1).order_by('-id')
    context = {
        'tracks': tracks,'videos':videos, 'newest_videos':newest_videos,'newest_tracks':newest_tracks
    }
    return render(request,template,context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fontend_topfive(request): 
    if 'member_id' in request.session:
        liked_videos=Video.objects.filter(is_approved=1).order_by('-like_counts').exclude(like_counts__isnull=True).exclude(like_counts=0)[:5]  
        liked_tracks=Tracks.objects.filter(is_approved=1).order_by('-like_counts').exclude(like_counts__isnull=True).exclude(like_counts=0)[:5]
        browsed_users=UserProfile.objects.all().order_by('-most_browsed').exclude(user_id=1).exclude(most_browsed__isnull=True).exclude(most_browsed=0)[:5]
        return render(request, 'frontend/topfive.html',{'liked_videos':liked_videos, 'liked_tracks': liked_tracks, 'browsed_users': browsed_users })
    else :
     return HttpResponseRedirect('/')  


