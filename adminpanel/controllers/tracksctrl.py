from django.shortcuts import render
from django.template import context,Template,Context
from adminpanel.models import *
from adminpanel.controllers.commonctrl import *
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
import os
from django.conf import settings
from django.views.decorators.cache import cache_control
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_upload_tracks(request):
    if 'admin_id' in request.session:
        genre = get_genre()
        types = get_type()
        if request.method == 'POST':
            import re
            title=request.POST.get('title', "NONE")
            subtitle=request.POST.get('subtitle', "NONE")
            track_image=request.FILES['track_image']
            track_file=request.FILES['track_file']
            genre_id=request.POST.get('genre_id', "NONE")
            #types_id=request.POST.get('types_id', "NONE")
            types_id = None
            dedicate=request.POST.get('dedicate', "NONE")
            #album_id=request.POST.get('album_id', "NONE")
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
                genre_id=int(genre_id),
                types_id=types_id,
                dedicate=dedicate,
                #album_id=album_id,
                uploadby_id=int(request.session['member_id']),
                is_approved=0
            )
            add_track.save()
            
            edit_link = "http://"+request.get_host()+"/admin/track-details/"+str(add_track.slug)
            approval_track_mail=EmailTemplates.objects.get(pk=6) 
            t = Template(approval_track_mail.templatebody)
            c = Context({'approval_text' : 'Track Approval' ,'edit_link' : edit_link })
            msg_html = t.render(c)
            send_mail(approval_track_mail.subject, 'hello world again', 'nawed@xigmapro.com', ['nawed@xigmapro.com'], html_message=msg_html)
            
            messages.add_message(request, messages.SUCCESS, 'Track uploaded waiting for approval!') 
            return HttpResponseRedirect('/pending-tracks/')    
        return render(request,'frontend/track-upload.html',{'genre':genre,'types':types})
    else :
        return HttpResponseRedirect('/admin/login/')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_pending_tracks(request,userid,likes_order=None):    
    if 'admin_id' in request.session:
        result=admin_pending_tracks(request,userid,likes_order)
        return render(request,'adminpanel/pending-tracks.html',{'pending_tracks':result,'user_id':userid,'likes_order':likes_order })
    else :
        return HttpResponseRedirect('/admin/login/')  
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_pending_tracks(request,likes_order=None):
    if 'admin_id' in request.session:
        result=admin_pending_tracks(request,"",likes_order)
        return render(request,'adminpanel/pending-tracks.html',{'pending_tracks':result,'user_id':None,'likes_order':likes_order  })
    else :
        return HttpResponseRedirect('/admin/login/')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_tracks(request,userid,likes_order=None):    
    if 'admin_id' in request.session:
        result=admin_my_tracks(request,userid,likes_order)
        return render(request,'adminpanel/track-listing.html',{'tracks':result,'user_id':userid,'likes_order':likes_order })
    else :
        return HttpResponseRedirect('/admin/login/')  
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_tracks(request,likes_order=None):
    if 'admin_id' in request.session:
        result=admin_my_tracks(request,"",likes_order)
        return render(request,'adminpanel/track-listing.html',{'tracks':result,'user_id':None,'likes_order':likes_order })
    else :
        return HttpResponseRedirect('/admin/login/')       
    

def admin_pending_tracks(request,userid,likes_order):   
    if userid:
        if likes_order == "asc":
            pending_tracks=Tracks.objects.filter(is_approved=0,album_id__isnull=True,uploadby_id=int(userid)).order_by('like_counts')
        elif likes_order == "desc":
           pending_tracks=Tracks.objects.filter(is_approved=0,album_id__isnull=True,uploadby_id=int(userid)).order_by('-like_counts') 
        else :
          pending_tracks=Tracks.objects.filter(is_approved=0,album_id__isnull=True,uploadby_id=int(userid))  
    else:
        if likes_order == "asc":
            pending_tracks=Tracks.objects.filter(is_approved=0,album_id__isnull=True).order_by('like_counts')
        elif likes_order == "desc":
            pending_tracks=Tracks.objects.filter(is_approved=0,album_id__isnull=True).order_by('-like_counts')
        else:
           pending_tracks=Tracks.objects.filter(is_approved=0,album_id__isnull=True) 
    
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
    return pending_tracks
   

def admin_my_tracks(request,userid,likes_order):   
    if userid:
        if likes_order == "asc":
            tracks=Tracks.objects.filter(is_approved=1,album_id__isnull=True,uploadby_id=int(userid)).order_by('like_counts')
        elif likes_order == "desc":
            tracks=Tracks.objects.filter(is_approved=1,album_id__isnull=True,uploadby_id=int(userid)).order_by('-like_counts')
        else:
           tracks=Tracks.objects.filter(is_approved=1,album_id__isnull=True,uploadby_id=int(userid)) 
    else:
        if likes_order == "asc":
            tracks=tracks=Tracks.objects.filter(is_approved=1,album_id__isnull=True).order_by('like_counts')
        elif likes_order == "desc":
            tracks=Tracks.objects.filter(is_approved=1,album_id__isnull=True).order_by('-like_counts')
        else:
           tracks=Tracks.objects.filter(is_approved=1,album_id__isnull=True)
        
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
    return tracks
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def admin_track_details(request,slug):    
    if 'admin_id' in request.session:
        if Tracks.objects.filter(slug=slug).exists():
            genre = get_genre()
            types = get_type()
            result=Tracks.objects.get(slug=slug)
            return render(request,'adminpanel/track-detail.html',{'track':result, 'genre':genre, 'types' : types })
        else :
           messages.add_message(request, messages.ERROR, 'Not the right track!')  
           return HttpResponseRedirect('/admin/tracks/')  
    else :
        return HttpResponseRedirect('/admin/login/') 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_track_edit(request):
    if 'admin_id' in request.session:
        if request.method == 'POST':
            track_id=request.POST['track_id']
            result_edit=Tracks.objects.get(pk=track_id)
            trk_title = result_edit.title
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
                      return HttpResponseRedirect('/admin/track-details/'+result_edit.slug+'/')  
                   else:
                        mail_text = trk_title+str(' is deleted by admin')
                        edit_link = ""
                        content_email('Your Track Deleted',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
                        messages.add_message(request, messages.SUCCESS, 'Track deleted successfully!')
                        
                        if result_edit.album_id is None: # normal track
                            return HttpResponseRedirect('/admin/tracks/')
                        else:
                            albumslug=Album.objects.get(pk=result_edit.album_id)  
                            return HttpResponseRedirect('/admin/album-details/'+albumslug.slug+'/')
                else:
                      messages.add_message(request, messages.ERROR, 'Not able to delete track!')
                      return HttpResponseRedirect('/admin/track-details/'+result_edit.slug+'/')
            elif 'btn_disapprove' in request.POST :  
                result_edit.is_approved = 0
                result_edit.save()
                
                mail_text = 'Track '+result_edit.title+str(' is disapproved by admin')
                edit_link = "http://"+request.get_host()+"/track-details/"+str(result_edit.slug)
                content_email('Your Track Disapproved',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
                
                messages.add_message(request, messages.SUCCESS, 'Track status change to disapprove!') 
                return HttpResponseRedirect('/admin/track-details/'+result_edit.slug+'/')
            elif 'btn_approve' in request.POST :  
                result_edit.is_approved = 1
                result_edit.save()
                
                mail_text = 'Track '+result_edit.title+str(' is approved by admin')
                edit_link = "http://"+request.get_host()+"/track-details/"+str(result_edit.slug)
                content_email('Your Track Approved',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
                
                messages.add_message(request, messages.SUCCESS, 'Track status change to approve')
                return HttpResponseRedirect('/admin/track-details/'+result_edit.slug+'/')
            
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
                
                mail_text = 'Track '+result_edit.title+str(' is edited by admin')
                edit_link = "http://"+request.get_host()+"/track-details/"+str(result_edit.slug)
                content_email('Your Track Edited',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
                messages.add_message(request, messages.SUCCESS, 'track edited successfully!')
                return HttpResponseRedirect('/admin/track-details/'+result_edit.slug+'/')
                       
            else :
               print("Action not allowed") 
        else :
            print("this not a post method")
            
    else :
        return HttpResponseRedirect('/admin/login/')    
        
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def track_delete(request):
    if request.method == 'POST':
        track_id=request.POST['track_id']
        result_edit=Tracks.objects.get(pk=track_id)
        trk_title = result_edit.title
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
                messages.add_message(request, messages.ERROR, 'Technical error!')
                return HttpResponse(0)
            else:
                mail_text = trk_title+str(' is deleted by admin')
                edit_link = ""
                content_email('Your Track Deleted',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
                messages.add_message(request, messages.SUCCESS, 'Track deleted successfully!')
                return HttpResponse(0)
        else:
            messages.add_message(request, messages.ERROR, 'Not able to delete track!')
            return HttpResponse(0)
           
@cache_control(no_cache=True, must_revalidate=True, no_store=True)            
def track_approve(request):
    if request.method == 'POST':
        track_id=request.POST['track_id']
        result_edit=Tracks.objects.get(pk=track_id)
        result_edit.is_approved = 1
        result_edit.save()
        
        mail_text = 'Track '+result_edit.title+str(' is approved by admin')
        edit_link = "http://"+request.get_host()+"/track-details/"+str(result_edit.slug)
        content_email('Your Track Approved',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
        
        messages.add_message(request, messages.SUCCESS, 'Track status change to approve!') 
        return HttpResponse("1")
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def track_disapprove(request):
    if request.method == 'POST': 
        track_id=request.POST['track_id']
        result_edit=Tracks.objects.get(pk=track_id)
        result_edit.is_approved = 0
        result_edit.save()
        
        mail_text = 'Track '+result_edit.title+str(' is disapproved by admin')
        edit_link = "http://"+request.get_host()+"/track-details/"+str(result_edit.slug)
        content_email('Your Track Disapproved',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
        
        messages.add_message(request, messages.SUCCESS, 'Track status change to disapprove!') 
        return HttpResponse("1")