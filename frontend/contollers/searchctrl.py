from django.shortcuts import render
from django.template import context,Template,Context
from adminpanel.models import *
from frontend.contollers.commonctrl import *
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.db import connection
from hashids import Hashids
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_type(request):
    hashids = Hashids(salt="amaan_ns",min_length=16)
    import json
    srch = request.GET['term']
    search_type = request.GET['search_type']
    results = []
    
    if search_type == "dedication":
        user_json = {}
        user_json['value'] = srch
        user_json['label'] = srch
        results.append(user_json)
        
    elif search_type == "artist_name":
        if UserProfile.objects.filter(name__icontains=srch).exists():
            rows = UserProfile.objects.filter(name__icontains=srch)
            for row in rows:
                res_json = {}
                res_json['value'] = hashids.encode(row.user_id)
                res_json['label'] = row.name
                results.append(res_json)
        else :
            res_json = {}
            res_json['value'] = "No Result"
            res_json['label'] = "No Result"
            results.append(res_json)
        
    elif search_type == "types":
        if Type.objects.filter(title__icontains=srch).exists():
            rows = Type.objects.filter(title__icontains=srch)
            for row in rows:
                res_json = {}
                res_json['value'] = hashids.encode(row.id)
                res_json['label'] = row.title
                results.append(res_json) 
        else:
            res_json = {}
            res_json['value'] = "No Result"
            res_json['label'] = "No Result"
            results.append(res_json)
    
    elif search_type == "genre":
        if Genre.objects.filter(title__icontains=srch).exists():
            rows = Genre.objects.filter(title__icontains=srch)
            for row in rows:
                res_json = {}
                res_json['value'] = hashids.encode(row.id)
                res_json['label'] = row.title
                results.append(res_json)  
        else:
            res_json = {}
            res_json['value'] = "No Result"
            res_json['label'] = "No Result"
            results.append(res_json)
    
    else :
        user_json = {}
        user_json['value'] = "No Result"
        user_json['label'] = "No Result"
        results.append(user_json)
    
    data = json.dumps(results)
    mimetype = 'application/json'    
    return HttpResponse(data, mimetype)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_all(request,search_type,search_id,searchtext):
    hashids = Hashids(salt="amaan_ns",min_length=16)
    if search_type != "dedication":
        try:
            tup = hashids.decode(search_id)
            search_id = str(tup[0])
        except:
            return HttpResponseRedirect('/')
    artists = []
    artist = []
    if search_type == "artist_name":
        cursor = connection.cursor()
        cursor.execute("select usr.username as userslug, up.name as username, up.user_id as artist_id, am.* from adminpanel_userprofile as up INNER JOIN adminpanel_album as am"+
        " ON up.user_id = am.uploadby_id"
        " INNER JOIN auth_user as usr ON usr.id = am.uploadby_id where am.uploadby_id = "+search_id+" and am.is_approved = 1 and usr.is_active = 1 ORDER BY am.id DESC " )
        albums = dictfetchall(cursor)
        
        cursor = connection.cursor()
        cursor.execute("select usr.username as userslug, up.name as username, up.user_id as artist_id, at.* from adminpanel_userprofile as up INNER JOIN adminpanel_tracks as at"+
        " ON up.user_id = at.uploadby_id" 
        " INNER JOIN auth_user as usr ON usr.id = at.uploadby_id where at.uploadby_id = "+search_id+" and at.is_approved = 1 and usr.is_active = 1 ORDER BY at.id DESC" )
        tracks = dictfetchall(cursor)
        
        cursor = connection.cursor()
        cursor.execute("select usr.username as userslug, up.name as username, up.user_id as artist_id, av.* from adminpanel_userprofile as up INNER JOIN adminpanel_video as av"+
        " ON up.user_id = av.uploadby_id"
        " INNER JOIN auth_user as usr ON usr.id = av.uploadby_id where av.uploadby_id = "+search_id+" and av.is_approved = 1 and usr.is_active = 1 ORDER BY av.id DESC" )
        videos = dictfetchall(cursor)
        
        uprofile_update = UserProfile.objects.get(user_id=int(search_id))
        most_browsed = int(uprofile_update.most_browsed)+int(1)
        uprofile_update.most_browsed=most_browsed
        uprofile_update.save()
        
    elif search_type == "types":
        cursor = connection.cursor()
        cursor.execute("select usr.username as userslug, up.name as username, up.user_id as artist_id, at.title,am.* from adminpanel_type as at INNER JOIN adminpanel_album as am ON at.id = am.types_id "
        " INNER JOIN auth_user as usr ON usr.id = am.uploadby_id"
        " INNER JOIN adminpanel_userprofile as up ON up.user_id = am.uploadby_id where am.types_id = "+search_id+" and am.is_approved = 1 ORDER BY am.id DESC" )
        albums = dictfetchall(cursor)
        for album in albums:
           artist.append(album['uploadby_id'])
        
        cursor = connection.cursor()
        cursor.execute("select usr.username as userslug, up.name as username, up.user_id as artist_id, at.title,atr.* from adminpanel_type as at INNER JOIN adminpanel_tracks as atr ON at.id = atr.types_id "
        " INNER JOIN auth_user as usr ON usr.id = atr.uploadby_id"
        " INNER JOIN adminpanel_userprofile as up ON up.user_id = atr.uploadby_id where atr.types_id = "+search_id+" and atr.is_approved = 1 ORDER BY atr.id DESC" )
        tracks = dictfetchall(cursor)
        for track in tracks:
           artist.append(track['uploadby_id'])
        
        cursor = connection.cursor()
        cursor.execute("select usr.username as userslug, up.name as username, up.user_id as artist_id, at.title,av.* from adminpanel_type as at INNER JOIN adminpanel_video as av ON at.id = av.types_id"
        " INNER JOIN auth_user as usr ON usr.id = av.uploadby_id"
        " INNER JOIN adminpanel_userprofile as up ON up.user_id = av.uploadby_id where av.types_id = "+search_id+" and av.is_approved = 1 ORDER BY av.id DESC" )
        videos = dictfetchall(cursor)   
        for video in videos:
           artist.append(video['uploadby_id'])
        
    elif search_type == "genre":
        cursor = connection.cursor()
        cursor.execute("select usr.username as userslug, up.name as username, up.user_id as artist_id, ag.title as genretitle, am.* from adminpanel_genre as ag INNER JOIN adminpanel_album as am ON ag.id = am.genre_id"
        " INNER JOIN auth_user as usr ON usr.id = am.uploadby_id"
        " INNER JOIN adminpanel_userprofile as up ON up.user_id = am.uploadby_id where am.genre_id = "+search_id+" and am.is_approved = 1 ORDER BY am.id DESC" )
        albums = dictfetchall(cursor)
        for album in albums:
           artist.append(album['uploadby_id'])
        
        cursor = connection.cursor()
        cursor.execute("select usr.username as userslug, up.name as username, up.user_id as artist_id, ag.title,atr.* from adminpanel_genre as ag INNER JOIN adminpanel_tracks as atr ON ag.id = atr.genre_id"
        " INNER JOIN auth_user as usr ON usr.id = atr.uploadby_id"
        " INNER JOIN adminpanel_userprofile as up ON up.user_id = atr.uploadby_id where atr.genre_id = "+search_id+" and atr.is_approved = 1 ORDER BY atr.id DESC" )
        tracks = dictfetchall(cursor)
        for track in tracks:
            artist.append(track['uploadby_id'])
        
        cursor = connection.cursor()
        cursor.execute("select usr.username as userslug, up.name as username, up.user_id as artist_id, ag.title,av.* from adminpanel_genre as ag INNER JOIN adminpanel_video as av ON ag.id = av.genre_id" 
        " INNER JOIN auth_user as usr ON usr.id = av.uploadby_id"
        " INNER JOIN adminpanel_userprofile as up ON up.user_id = av.uploadby_id where av.genre_id = "+search_id+" and av.is_approved = 1 ORDER BY av.id DESC" )
        videos = dictfetchall(cursor)    
        for video in videos:
           artist.append(video['uploadby_id'])
        
    elif search_type == "dedication":
        cursor = connection.cursor()
        cursor.execute("select usr.username as userslug, up.name as username, up.user_id as artist_id, am.* from adminpanel_album as am" 
        " INNER JOIN auth_user as usr ON usr.id = am.uploadby_id"
        " INNER JOIN adminpanel_userprofile as up ON up.user_id = am.uploadby_id where am.dedicate like "+"'%"+searchtext+"%'"+" and am.is_approved = 1 ORDER BY am.id DESC" )
        albums = dictfetchall(cursor)
        for album in albums:
           artist.append(album['uploadby_id'])
        
        cursor = connection.cursor()
        cursor.execute("select usr.username as userslug, up.name as username, up.user_id as artist_id, atr.* from adminpanel_tracks as atr" 
        " INNER JOIN auth_user as usr ON usr.id = atr.uploadby_id"
        " INNER JOIN adminpanel_userprofile as up ON up.user_id = atr.uploadby_id where atr.dedicate like "+"'%"+searchtext+"%'"+" and atr.is_approved = 1 ORDER BY atr.id DESC" )
        tracks = dictfetchall(cursor)
        for track in tracks:
           artist.append(track['uploadby_id'])
        
        cursor = connection.cursor()
        cursor.execute("select usr.username as userslug, up.name as username, up.user_id as artist_id, av.* from adminpanel_video as av"
        " INNER JOIN auth_user as usr ON usr.id = av.uploadby_id"
        " INNER JOIN adminpanel_userprofile as up ON up.user_id = av.uploadby_id where av.dedicate like "+"'%"+searchtext+"%'"+" and av.is_approved = 1 ORDER BY av.id DESC" )
        videos = dictfetchall(cursor) 
        for video in videos:
           artist.append(video['uploadby_id'])
        
    else :
        albums = None
        tracks = None
        videos = None
    
    
    artist = set(artist) 
    artist = list(artist)
    artist = ','.join(map(str, artist))
    
    if artist :
        cursor.execute("select usr.*,up.* from adminpanel_userprofile as up INNER JOIN auth_user as usr ON up.user_id = usr.id  where up.user_id IN ("+artist+") " )
        #cursor.execute("select up.* from adminpanel_userprofile as up where up.user_id IN ("+artist+") " )
        artists = dictfetchall(cursor)
    else :
        artist = []
        artists = []
      
    return render(request,'frontend/search.html',{ 'albums': albums,'tracks': tracks, 'videos': videos, 'artists' : artists, 'artist':artist, 'searchtext':searchtext })    


   
         
        
    
    
        