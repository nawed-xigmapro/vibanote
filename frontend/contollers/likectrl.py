from django.shortcuts import render
from django.template import context,Context,Template
from django.http import HttpResponse
from adminpanel.models import *
from frontend.contollers.commonctrl import *
# Create your views here.
def like_it(request):
    if 'member_id' in request.session:
        if request.POST:
            import json
            res_json = {}
            lid=request.POST.get('lid', "NONE")
            ltype=request.POST.get('ltype', "NONE")
            if ltype == 'album':
                if Likes.objects.filter(album_id=lid,user_id=int(request.session['member_id'])).exists():
                    Likes.objects.filter(album_id=lid,user_id=int(request.session['member_id'])).delete()
                    c = Likes.objects.filter(album_id=lid,user_id=int(request.session['member_id'])).count()
                    if c:
                       res_json['msg'] = "Not able to unlike technical error!"
                       res_json['Ack'] = "0"
                       res_json['likes'] = "0"
                       res_json['msg_type'] = "error"
                       return HttpResponse(json.dumps(res_json))    
                    else:
                       albc = Likes.objects.filter(album_id=lid).count()
                       album_likesup=Album.objects.get(pk=lid)
                       album_likesup.like_counts = albc
                       album_likesup.save()
                       res_json['msg'] = "you unlike it"
                       res_json['Ack'] = "1"
                       res_json['likes'] = albc
                       res_json['msg_type'] = "success"
                       return HttpResponse(json.dumps(res_json))
                else:
                    add_likes = Likes(
                        user_id=int(request.session['member_id']),
                        album_id=lid
                    )
                    add_likes.save()
                    if add_likes.id:
                        albc = Likes.objects.filter(album_id=lid).count()  
                        album_likes=Album.objects.get(pk=lid)
                        album_likes.like_counts = albc
                        album_likes.save()
                        res_json['msg'] = "you Liked it"
                        res_json['Ack'] = "1"
                        res_json['likes'] = albc
                        res_json['msg_type'] = "success"
                        return HttpResponse(json.dumps(res_json))

            elif ltype == 'track': 
                if Likes.objects.filter(track_id=lid,user_id=int(request.session['member_id'])).exists():
                    Likes.objects.filter(track_id=lid,user_id=int(request.session['member_id'])).delete()
                    c = Likes.objects.filter(track_id=lid,user_id=int(request.session['member_id'])).count()
                    if c:
                       res_json['msg'] = "Not able to unlike technical error!"
                       res_json['Ack'] = "0"
                       res_json['likes'] = "0" 
                       res_json['msg_type'] = "error"
                       return HttpResponse(json.dumps(res_json))    
                    else:
                       albc = Likes.objects.filter(track_id=lid).count()
                       album_likesup=Tracks.objects.get(pk=lid)
                       album_likesup.like_counts = albc
                       album_likesup.save()
                       res_json['msg'] = "you unlike it"
                       res_json['Ack'] = "1"
                       res_json['likes'] = albc 
                       res_json['msg_type'] = "success"
                       return HttpResponse(json.dumps(res_json))
                else:
                    add_likes = Likes(
                        user_id=int(request.session['member_id']),
                        track_id=lid
                    )
                    add_likes.save()
                    if add_likes.id:
                        albc = Likes.objects.filter(track_id=lid).count()  
                        album_likes=Tracks.objects.get(pk=lid)
                        album_likes.like_counts = albc
                        album_likes.save()
                        res_json['msg'] = "you Liked it"
                        res_json['Ack'] = "1"
                        res_json['likes'] = albc
                        res_json['msg_type'] = "success"
                        return HttpResponse(json.dumps(res_json))   
            
            elif ltype == 'video': 
                if Likes.objects.filter(video_id=lid,user_id=int(request.session['member_id'])).exists():
                    Likes.objects.filter(video_id=lid,user_id=int(request.session['member_id'])).delete()
                    c = Likes.objects.filter(video_id=lid,user_id=int(request.session['member_id'])).count()
                    if c:
                       res_json['msg'] = "Not able to unlike technical error!"
                       res_json['Ack'] = "0"
                       res_json['likes'] = "0" 
                       res_json['msg_type'] = "error"
                       return HttpResponse(json.dumps(res_json))    
                    else:
                       albc = Likes.objects.filter(video_id=lid).count()
                       album_likesup=Video.objects.get(pk=lid)
                       album_likesup.like_counts = albc
                       album_likesup.save()
                       res_json['msg'] = "you unlike it"
                       res_json['Ack'] = "1"
                       res_json['likes'] = albc 
                       res_json['msg_type'] = "success"
                       return HttpResponse(json.dumps(res_json))
                else:
                    add_likes = Likes(
                        user_id=int(request.session['member_id']),
                        video_id=lid
                    )
                    add_likes.save()
                    if add_likes.id:
                        albc = Likes.objects.filter(video_id=lid).count()  
                        album_likes=Video.objects.get(pk=lid)
                        album_likes.like_counts = albc
                        album_likes.save()
                        res_json['msg'] = "you Liked it"
                        res_json['Ack'] = "1"
                        res_json['likes'] = albc
                        res_json['msg_type'] = "success"
                        return HttpResponse(json.dumps(res_json))  
            
            elif ltype == 'user': 
                if Likes.objects.filter(artist_id=lid,user_id=int(request.session['member_id'])).exists():
                    Likes.objects.filter(artist_id=lid,user_id=int(request.session['member_id'])).delete()
                    c = Likes.objects.filter(artist_id=lid,user_id=int(request.session['member_id'])).count()
                    if c:
                       res_json['msg'] = "Not able to unlike technical error!"
                       res_json['Ack'] = "0"
                       res_json['likes'] = "0" 
                       res_json['msg_type'] = "error"
                       return HttpResponse(json.dumps(res_json))    
                    else:
                       albc = Likes.objects.filter(artist_id=lid).count()
                       atrist_likesup=UserProfile.objects.get(user_id=lid)
                       atrist_likesup.like_counts = albc
                       atrist_likesup.save()
                       res_json['msg'] = "you unlike it"
                       res_json['Ack'] = "1"
                       res_json['likes'] = albc 
                       res_json['msg_type'] = "success"
                       return HttpResponse(json.dumps(res_json))       
                else:
                    add_likes = Likes(
                        user_id=int(request.session['member_id']),
                        artist_id=lid
                    )
                    add_likes.save()
                    if add_likes.id:
                        albc = Likes.objects.filter(artist_id=lid).count()  
                        atrist_likes=UserProfile.objects.get(user_id=lid)
                        atrist_likes.like_counts = albc
                        atrist_likes.save()
                        res_json['msg'] = "you Liked it"
                        res_json['Ack'] = "1"
                        res_json['likes'] = albc 
                        res_json['msg_type'] = "success"
                        return HttpResponse(json.dumps(res_json))

            else:   
               res_json['msg'] = "Types not match"
               res_json['Ack'] = "0"
               res_json['likes'] = "0" 
               res_json['msg_type'] = "error"
               return HttpResponse(json.dumps(res_json))
        else:
            res_json['msg'] = "Not in Post"
            res_json['Ack'] = "0"
            res_json['likes'] = "0" 
            res_json['msg_type'] = "error"
            return HttpResponse(json.dumps(res_json))
    else :
        res_json['msg'] = "Not in Session"
        res_json['Ack'] = "0"
        res_json['likes'] = "0" 
        res_json['msg_type'] = "error"
        return HttpResponse(json.dumps(res_json))
    


        
           
           