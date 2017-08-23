from django.template import context,Template,Context
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db import connection
from django.utils import formats
from adminpanel.models import *
from django.contrib import messages
from datetime import datetime, timedelta
from adminpanel.controllers.commonctrl import *
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def analytics_registration(request):
    if 'admin_id' in request.session:
        sevendays_users = User.objects.filter(date_joined__gte=datetime.now()-timedelta(days=7)).exclude(pk=1).count() 
        thirtydays_users = User.objects.filter(date_joined__gte=datetime.now()-timedelta(days=30)).exclude(pk=1).count()
        ninetydays_users = User.objects.filter(date_joined__gte=datetime.now()-timedelta(days=90)).exclude(pk=1).count()
        alltime_users = User.objects.all().exclude(pk=1).count() 
        return render(request, 'adminpanel/analytics-registration.html',{'sevendays_users':sevendays_users,'thirtydays_users':thirtydays_users,'ninetydays_users':ninetydays_users,'alltime_users':alltime_users})
    else :
     return HttpResponseRedirect('/admin/login/') 
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_customdates(request): 
    if 'admin_id' in request.session:
        if request.method == 'POST':
            import json
            rtn_obj = {}
            start_date = datetime.strptime(request.POST.get('start_date', None), '%Y-%m-%d')
            end_date = datetime.strptime(request.POST.get('end_date', None), '%Y-%m-%d')
            end_date = end_date + timedelta(days=1)
            customdates_users=User.objects.filter(date_joined__range=[start_date, end_date]).exclude(pk=1).count() 
            if customdates_users :
                rtn_obj['ack'] = "1"
                rtn_obj['msg'] = "Number of Users"
                rtn_obj['count'] = customdates_users
                data = json.dumps(rtn_obj)
                return HttpResponse(data) 
            else:
                rtn_obj['ack'] = "0"
                rtn_obj['msg'] = "No users found."
                rtn_obj['count'] = "0"
                data = json.dumps(rtn_obj)
                return HttpResponse(data) 
        else:
            rtn_obj['ack'] = "0"
            rtn_obj['msg'] = "No the right method."
            rtn_obj['count'] = "0"
            data = json.dumps(rtn_obj)
            return HttpResponse(data)     
    else :
        rtn_obj['ack'] = "0"
        rtn_obj['msg'] = "user out of session."
        rtn_obj['count'] = "0"
        data = json.dumps(rtn_obj)
        return HttpResponse(data) 

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def analytics_user_status(request):
    if 'admin_id' in request.session:
        active_users = User.objects.filter(is_active=1).exclude(pk=1).count() 
        inactive_users = User.objects.filter(is_active=0).exclude(pk=1).count()
        return render(request, 'adminpanel/analytics-userstatus.html',{'active_users':active_users,'inactive_users':inactive_users })
    else :
     return HttpResponseRedirect('/admin/login/')  
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def analytics_albumuploads(request):
    if 'admin_id' in request.session:
        sevendays_albums = Album.objects.filter(created_date__gte=datetime.now()-timedelta(days=7)).count() 
        thirtydays_albums = Album.objects.filter(created_date__gte=datetime.now()-timedelta(days=30)).count()
        ninetydays_albums = Album.objects.filter(created_date__gte=datetime.now()-timedelta(days=90)).count()
        alltime_albums = Album.objects.all().count() 
        return render(request, 'adminpanel/analytics-album.html',{'sevendays_albums':sevendays_albums,'thirtydays_albums':thirtydays_albums,'ninetydays_albums':ninetydays_albums,'alltime_albums':alltime_albums})
    else :
     return HttpResponseRedirect('/admin/login/') 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def analytics_trackuploads(request):
    if 'admin_id' in request.session:
        sevendays_tracks = Tracks.objects.filter(created_date__gte=datetime.now()-timedelta(days=7)).count() 
        thirtydays_tracks = Tracks.objects.filter(created_date__gte=datetime.now()-timedelta(days=30)).count()
        ninetydays_tracks = Tracks.objects.filter(created_date__gte=datetime.now()-timedelta(days=90)).count()
        alltime_tracks = Tracks.objects.all().count() 
        return render(request, 'adminpanel/analytics-tracks.html',{'sevendays_tracks':sevendays_tracks,'thirtydays_tracks':thirtydays_tracks,'ninetydays_tracks':ninetydays_tracks,'alltime_tracks':alltime_tracks})
    else :
     return HttpResponseRedirect('/admin/login/') 
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def analytics_videouploads(request):
    if 'admin_id' in request.session:
        sevendays_video = Video.objects.filter(created_date__gte=datetime.now()-timedelta(days=7)).count() 
        thirtydays_video = Video.objects.filter(created_date__gte=datetime.now()-timedelta(days=30)).count()
        ninetydays_video = Video.objects.filter(created_date__gte=datetime.now()-timedelta(days=90)).count()
        alltime_video = Video.objects.all().count() 
        return render(request, 'adminpanel/analytics-videos.html',{'sevendays_video':sevendays_video,'thirtydays_video':thirtydays_video,'ninetydays_video':ninetydays_video,'alltime_video':alltime_video})
    else :
     return HttpResponseRedirect('/admin/login/')  
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def countrywise_users(request): 
    if 'admin_id' in request.session:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT( au.user_id ) AS users, ac.name AS country_name"
                        " FROM adminpanel_userprofile AS au"
                        " INNER JOIN adminpanel_countries AS ac ON au.country = ac.id"
                        " WHERE au.user_id !=1"
                        " GROUP BY ac.id")
        countryusers = dictfetchall(cursor)                
        return render(request, 'adminpanel/analytics-usercountry.html',{'countryusers':countryusers})
    else :
     return HttpResponseRedirect('/admin/login/') 
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def analytics_topcountries(request): 
    if 'admin_id' in request.session:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT( au.user_id ) AS users, ac.name AS country_name"
                        " FROM adminpanel_userprofile AS au"
                        " INNER JOIN adminpanel_countries AS ac ON au.country = ac.id"
                        " WHERE au.user_id !=1"
                        " GROUP BY ac.id"
                        " ORDER BY COUNT( au.user_id ) DESC"
                        " LIMIT 5")
        top_countries = dictfetchall(cursor)                
        return render(request, 'adminpanel/analytics-topcountries.html',{'top_countries':top_countries})
    else :
     return HttpResponseRedirect('/admin/login/')  
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def analytics_mostliked(request): 
    if 'admin_id' in request.session:
        liked_users=UserProfile.objects.all().order_by('-like_counts').exclude(user_id=1).exclude(like_counts__isnull=True).exclude(like_counts=0)[:5]  
        liked_tracks=Tracks.objects.filter(is_approved=1).order_by('-like_counts').exclude(like_counts__isnull=True).exclude(like_counts=0)[:5]
        liked_albums=Album.objects.filter(is_approved=1).order_by('-like_counts').exclude(like_counts__isnull=True).exclude(like_counts=0)[:5]
        return render(request, 'adminpanel/analytics-mostliked.html',{'liked_users':liked_users, 'liked_tracks': liked_tracks, 'liked_albums': liked_albums })
    else :
     return HttpResponseRedirect('/admin/login/')  
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def analytics_mostbrowsed(request): 
    if 'admin_id' in request.session:
        browsed_users=UserProfile.objects.all().order_by('-most_browsed').exclude(user_id=1).exclude(most_browsed__isnull=True).exclude(most_browsed=0)[:5]  
        return render(request, 'adminpanel/analytics-mostbrowsed.html',{'browsed_users':browsed_users })
    else :
     return HttpResponseRedirect('/admin/login/')  
