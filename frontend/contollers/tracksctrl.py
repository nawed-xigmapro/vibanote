from django.shortcuts import render
from django.template import context,Template,Context
from adminpanel.models import *
from frontend.contollers.commonctrl import *
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db import connection
import os
from django.conf import settings
from django.views.decorators.cache import cache_control
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload_tracks(request):
    if 'member_id' in request.session:
        genre = get_genre()
        types = get_type()
        if request.method == 'POST':
            import re
            title=request.POST.get('title', "NONE")
            subtitle=request.POST.get('subtitle', "NONE")
            #track_image=request.FILES['track_image']
            track_image = None
            track_file=request.FILES['track_file']
            album_id=request.POST.get('album_id', "NONE")
            album_slug=request.POST.get('album_slug', "NONE")
            
            if len(request.FILES) != 0:
                if 'track_image' in request.FILES:  
                    track_image = request.FILES['track_image']
            
            if 'album_slug' not in request.POST: # normal track
                genre_id=int(request.POST.get('genre_id', None))
                #types_id=int(request.POST.get('types_id', None))
                types_id = None
                dedicate=request.POST.get('dedicate', None)
            else :
                genre_id = None
                types_id = None
                dedicate = None
                
            create_slug = title.lower()
            create_slug = create_slug.replace (" ", "-")
            create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
            
            if Tracks.objects.filter(slug=create_slug).exists():
                count_slugs = Tracks.objects.filter(slug__contains=create_slug).count()
                create_slug = create_slug+"-"+str(count_slugs)
            
            add_track = Tracks(
                title=title,
                slug=create_slug,
                subtitle=subtitle,
                track_image=track_image,
                track_file=track_file,
                genre_id=genre_id,
                types_id=types_id,
                dedicate=dedicate,
                album_id=album_id,
                uploadby_id=int(request.session['member_id']),
                is_approved=0
            )
            add_track.save()
            admininfo = ns_get_user(1)
            if 'album_slug' not in request.POST: # normal track
                edit_link = "http://"+request.get_host()+"/admin/track-details/"+str(add_track.slug)
                approval_track_mail=EmailTemplates.objects.get(pk=6) 
                t = Template(approval_track_mail.templatebody)
                c = Context({'approval_text' : 'Track Approval' ,'edit_link' : edit_link })
                msg_html = t.render(c)
                send_mail(approval_track_mail.subject, 'hello world again', admininfo.email, [admininfo.email], html_message=msg_html)
                messages.add_message(request, messages.SUCCESS, 'Track uploaded waiting for approval!') 
                return HttpResponseRedirect('/pending-tracks/')
            
            else: # album track
                if Tracks.objects.filter(album_id=int(album_id)).exists():
                    c = Tracks.objects.filter(album_id=int(album_id)).count()
                    if c <= 1:
                        show_msg = "Track uploaded Successfully,album waiting for approval."
                        edit_link = "http://"+request.get_host()+"/admin/album-details/"+str(album_slug)
                        approval_track_mail=EmailTemplates.objects.get(pk=6) 
                        t = Template(approval_track_mail.templatebody)
                        c = Context({'approval_text' : 'Album Approval' ,'edit_link' : edit_link })
                        msg_html = t.render(c)
                        send_mail(approval_track_mail.subject, 'hello world again', admininfo.email, [admininfo.email], html_message=msg_html)  
                    else:
                        show_msg = "Track uploaded Successfully!"
                messages.add_message(request, messages.SUCCESS, show_msg)  
                return HttpResponseRedirect('/album-details/'+album_slug+'/')  
           
        return render(request,'frontend/track-upload.html',{'genre':genre,'types':types})
    else :
        return HttpResponseRedirect('/')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pending_tracks(request):   
    if 'member_id' in request.session:
        pending_tracks=Tracks.objects.filter(is_approved=0,album_id__isnull=True,uploadby_id=int(request.session['member_id']))
        paginator = Paginator(pending_tracks, 12) # Show 10 contacts per page
        page = request.GET.get('page')
        try:
            pending_tracks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pending_tracks = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            pending_tracks = paginator.page(paginator.num_pages)
        return render(request,'frontend/pending-tracks.html',{'pending_tracks':pending_tracks })
    else :
        return HttpResponseRedirect('/')  
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def my_tracks(request):   
    if 'member_id' in request.session:
        tracks=Tracks.objects.filter(is_approved=1,album_id__isnull=True,uploadby_id=int(request.session['member_id']))
        paginator = Paginator(tracks, 12) # Show 10 contacts per page
        page = request.GET.get('page')
        try:
            tracks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            tracks = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            tracks = paginator.page(paginator.num_pages)
        return render(request,'frontend/my-tracks.html',{'tracks':tracks })
    else :
        return HttpResponseRedirect('/')     
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def track_details(request,slug):    
    if 'member_id' in request.session:
        if Tracks.objects.filter(slug=slug,uploadby_id=int(request.session['member_id'])).exists():
            genre = get_genre()
            types = get_type()
            result=Tracks.objects.get(slug=slug)
            return render(request,'frontend/track-detail.html',{'track':result, 'genre':genre, 'types' : types })
        else :
           messages.add_message(request, messages.ERROR, 'Not the right track!')  
           return HttpResponseRedirect('/dashboard/')  
    else :
        return HttpResponseRedirect('/') 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def track_edit(request):
    if 'member_id' in request.session:
        if request.method == 'POST':
            track_id=request.POST['track_id']
            result_edit=Tracks.objects.get(pk=track_id)
            if 'btn_delete' in request.POST :  
                if Tracks.objects.filter(pk=int(track_id)).exists():
                   if(result_edit.track_image):
                            image_path = settings.MEDIA_ROOT+"/"+result_edit.track_image.name
                            if os.path.isfile(image_path):
                                os.unlink(image_path)     
                     
                   if(result_edit.track_file):
                            image_pathf = settings.MEDIA_ROOT+"/"+result_edit.track_file.name
                            if os.path.isfile(image_pathf):
                                os.unlink(image_pathf)            
                   Tracks.objects.filter(pk=int(track_id)).delete()
                   c = Tracks.objects.filter(pk=int(track_id)).count()
                   if c:
                      messages.add_message(request, messages.ERROR, 'Not able to delete track!') 
                      return HttpResponseRedirect('/track-details/'+result_edit.slug+'/')  
                   else:
                        messages.add_message(request, messages.SUCCESS, 'Track deleted successfully!')
                        if result_edit.album_id is None:
                            return HttpResponseRedirect('/my-tracks/')
                        else:
                          albumslug=Album.objects.get(pk=result_edit.album_id)  
                          return HttpResponseRedirect('/album-details/'+albumslug.slug+'/')  
                else:
                      messages.add_message(request, messages.ERROR, 'Not able to delete track!')
                      return HttpResponseRedirect('/track-details/'+result_edit.slug+'/')
            elif 'btn_edit' in request.POST :  
                import re
                title=request.POST.get('title', None)
                subtitle=request.POST.get('subtitle', None)
                
                if result_edit.album_id is None: # normal track
                    genre_id=request.POST.get('genre_id', None)
                    #types_id=request.POST.get('types_id', None)
                    types_id = None
                    dedicate=request.POST.get('dedicate', None)
                else: # album track
                   genre_id = None
                   types_id = None
                   dedicate = None
                
                create_slug = title.lower()
                create_slug = create_slug.replace (" ", "-")
                create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
                if Tracks.objects.filter(slug=create_slug).exists():
                    _slugcheck=Tracks.objects.get(slug=create_slug)
                    if _slugcheck.id!=int(track_id):
                       count_slugs = Tracks.objects.filter(slug__contains=create_slug).count()
                       create_slug = create_slug+"-"+str(count_slugs)
                
                result_edit.title = title
                result_edit.slug = create_slug
                result_edit.subtitle = subtitle
                result_edit.genre_id = genre_id
                result_edit.types_id = types_id
                result_edit.dedicate = dedicate
                result_edit.is_approved = 0
                result_edit.save()
                
                if len(request.FILES) != 0:
                    if 'track_image' in request.FILES:  
                        if(result_edit.track_image):
                            image_path = settings.MEDIA_ROOT+"/"+result_edit.track_image.name
                            if os.path.isfile(image_path):
                                os.unlink(image_path)                       
                        track_image = request.FILES['track_image']
                        result_edit.track_image = track_image
                        result_edit.save()
                    if 'track_file' in request.FILES:    
                        if(result_edit.track_file):
                            image_pathf = settings.MEDIA_ROOT+"/"+result_edit.track_file.name
                            if os.path.isfile(image_pathf):
                                os.unlink(image_pathf)
                        track_file = request.FILES['track_file']
                        result_edit.track_file = track_file
                        result_edit.save()            
                if result_edit.album_id is None:
                    admininfo = ns_get_user(1)
                    edit_link = "http://"+request.get_host()+"/admin/track-details/"+str(result_edit.slug)
                    approval_track_mail=EmailTemplates.objects.get(pk=6) 
                    t = Template(approval_track_mail.templatebody)
                    c = Context({'approval_text' : 'Track Approval','edit_link' : edit_link })
                    msg_html = t.render(c)
                    send_mail(approval_track_mail.subject, 'hello world again', admininfo.email, [admininfo.email], html_message=msg_html)
                if result_edit.album_id is None:
                    messages.add_message(request, messages.SUCCESS, 'track edited successfully waiting for approval!')
                else:
                    messages.add_message(request, messages.SUCCESS, 'track edited successfully!')
                return HttpResponseRedirect('/track-details/'+result_edit.slug+'/')
                       
            else :
               print("Action not allowed") 
        else :
            print("this not a post method")
            
    else :
        return HttpResponseRedirect('/')    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def singletrack_delete(request):
    if request.method == 'POST' :  
        import json
        rtn_obj = {}
        track_id=request.POST['track_id']
        if Tracks.objects.filter(pk=int(track_id)).exists():
            del_track=Tracks.objects.get(pk=int(track_id))
            if(del_track.track_file):
                track_path = settings.MEDIA_ROOT+"/"+del_track.track_file.name
                if os.path.isfile(track_path):
                    os.unlink(track_path)  
            if(del_track.track_image):        
                image_path = settings.MEDIA_ROOT+"/"+del_track.track_image.name
                if os.path.isfile(image_path):
                    os.unlink(image_path)     
            Tracks.objects.filter(pk=int(track_id)).delete()
            c = Tracks.objects.filter(pk=int(track_id)).count()
            if c:
                rtn_obj['ack'] = "0"
                rtn_obj['msg'] = "Technical Error track cannot be deleted!"
                data = json.dumps(rtn_obj)
                return HttpResponse(data) 
            else:
                rtn_obj['ack'] = "1"
                rtn_obj['msg'] = "Track Deleted successfully!"
                messages.add_message(request, messages.SUCCESS, 'Track Deleted successfully!')
                data = json.dumps(rtn_obj)
                return HttpResponse(data)
        else:
            rtn_obj['ack'] = "0"
            rtn_obj['msg'] = "Track doesnot exists to delete!"
            data = json.dumps(rtn_obj)
            return HttpResponse(data)
    else:
        rtn_obj['ack'] = "0"
        rtn_obj['msg'] = "It is not a right method!"
        data = json.dumps(rtn_obj)
        return HttpResponse(data)      
    

def public_track_detail(request,trackslug):   
    if Tracks.objects.filter(slug=trackslug,is_approved=1).exists(): 
        #track_details=Tracks.objects.get(slug=trackslug,is_approved=1)
        cursor = connection.cursor()
        cursor.execute("select au.username,up.name,up.user_id,up.picture,at.*,ag.title as genretitle from adminpanel_tracks as at INNER JOIN adminpanel_userprofile as up on up.user_id=at.uploadby_id"
        " INNER JOIN auth_user as au  ON au.id = up.user_id" 
        " INNER JOIN adminpanel_genre as ag  ON at.genre_id = ag.id" 
        " where at.is_approved=1 and at.slug = '"+str(trackslug)+"'")  
        track_details=query_to_dicts(cursor)
        return render(request,'frontend/public_track_detail.html',{'track_details':track_details})     
    else:
       messages.add_message(request, messages.ERROR, 'Track not found!') 
       return HttpResponseRedirect('/')  
        