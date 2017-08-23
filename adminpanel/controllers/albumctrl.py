from django.shortcuts import render
from django.template import context,Template,Context
from adminpanel.models import *
from frontend.contollers.commonctrl import *
from adminpanel.controllers.commonctrl import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
import os
from django.conf import settings
from django.views.decorators.cache import cache_control
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_album(request):
    if 'member_id' in request.session:
        genre = get_genre()
        types = get_type()
        if request.method == 'POST':
            import re
            title=request.POST.get('title', "NONE")
            subtitle=request.POST.get('subtitle', "NONE")
            album_image=request.FILES['album_image']
            genre_id=request.POST.get('genre_id', "NONE")
            types_id=request.POST.get('types_id', "NONE")
            dedicate=request.POST.get('dedicate', "NONE")
            create_slug = title.lower()
            create_slug = create_slug.replace (" ", "-")
            create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
            
            if Album.objects.filter(slug=create_slug).exists():
                count_slugs = Album.objects.filter(slug__contains=create_slug).count()
                create_slug = create_slug+"-"+str(count_slugs)
            
            album_add = Album(
                title=title,
                slug=create_slug,
                subtitle=subtitle,
                album_image=album_image,
                genre_id=int(genre_id),
                types_id=int(types_id),
                dedicate=dedicate,
                uploadby_id=int(request.session['member_id']),
                is_approved=0,
                is_edited=0
            )
            album_add.save()
            
            messages.add_message(request, messages.SUCCESS, 'Album added please add tracks!') 
            return HttpResponseRedirect('/album-details/'+str(album_add.slug)+'/')    
        return render(request,'frontend/add-album.html',{'genre':genre,'types':types})
    else :
        return HttpResponseRedirect('/')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_albums_list(request,userid,likes_order=None):   
    if 'admin_id' in request.session:
        if userid :
            if likes_order == "asc":
                albums=Album.objects.filter(is_approved=1,uploadby_id=int(userid)).order_by('like_counts')
            elif likes_order == "desc" :
                albums=Album.objects.filter(is_approved=1,uploadby_id=int(userid)).order_by('-like_counts')
            else:
               albums=Album.objects.filter(is_approved=1,uploadby_id=int(userid)) 
               
            paginator = Paginator(albums, 12) # Show 10 contacts per page
            page = request.GET.get('page')
            try:
                albums = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                albums = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                albums = paginator.page(paginator.num_pages)
            return render(request,'adminpanel/albumlist.html',{'albums':albums,'user_id':userid,'likes_order':likes_order })
        else :
           return HttpResponseRedirect('/admin/login/') 
    else :
        return HttpResponseRedirect('/admin/login/') 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def albums_list(request,likes_order=None):   
    if 'admin_id' in request.session:
        if likes_order == "asc":
            albums=Album.objects.filter(is_approved=1).order_by('like_counts')
        elif likes_order == "desc" :
            albums=Album.objects.filter(is_approved=1).order_by('-like_counts')
        else:
            albums=Album.objects.filter(is_approved=1)
            
        paginator = Paginator(albums, 12) # Show 10 contacts per page
        page = request.GET.get('page')
        try:
            albums = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            albums = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            albums = paginator.page(paginator.num_pages)
        return render(request,'adminpanel/albumlist.html',{'albums':albums,'user_id':None,'likes_order':likes_order })
    else :
        return HttpResponseRedirect('/admin/login/')   
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pending_albums_list(request,userid=None,likes_order=None):   
    if 'admin_id' in request.session:
        if userid:
            if likes_order == "asc":
                pending_albums=Album.objects.filter(is_approved=0,uploadby_id=int(userid)).order_by('like_counts')
            elif likes_order == "desc":   
                pending_albums=Album.objects.filter(is_approved=0,uploadby_id=int(userid)).order_by('-like_counts')
            else:
               pending_albums=Album.objects.filter(is_approved=0,uploadby_id=int(userid)) 
        else:
            if likes_order == "asc":
                pending_albums=Album.objects.filter(is_approved=0).order_by('like_counts')
            elif likes_order == "desc":   
                pending_albums=Album.objects.filter(is_approved=0).order_by('-like_counts')
            else:
               pending_albums=Album.objects.filter(is_approved=0) 
                
        paginator = Paginator(pending_albums, 12) # Show 10 contacts per page
        page = request.GET.get('page')
        try:
            pending_albums = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pending_albums = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            pending_albums = paginator.page(paginator.num_pages)
        return render(request,'adminpanel/pending-albums.html',{'pending_albums':pending_albums,'user_id':userid,'likes_order':likes_order })
    else :
        return HttpResponseRedirect('/admin/login/')     
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def album_details(request,slug):    
    if 'admin_id' in request.session:
        if Album.objects.filter(slug=slug).exists():
            genre = get_genre()
            types = get_type()
            result=Album.objects.get(slug=slug)
            albumtracks=Tracks.objects.filter(album_id=result.id)
            return render(request,'adminpanel/album-detail.html',{'album':result, 'albumtracks':albumtracks ,'genre':genre, 'types' : types })
        else :
           messages.add_message(request, messages.ERROR, 'Not the right album!')  
           return HttpResponseRedirect('/admin/artists/')  
    else :
        return HttpResponseRedirect('/admin/login/') 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def album_edit(request):
    if 'admin_id' in request.session:
        if request.method == 'POST':
            album_id=request.POST['album_id']
            result_edit=Album.objects.get(pk=album_id)
            album_title = result_edit.title
            album_owner = result_edit.uploadby_id
            if 'btn_delete' in request.POST :  
                if Album.objects.filter(pk=int(album_id)).exists():
                    if Tracks.objects.filter(album_id=int(album_id)).exists():
                        del_tracks=Tracks.objects.filter(album_id=int(album_id))
                        for del_track in del_tracks:
                            if(del_track.track_image):
                                image_path = settings.MEDIA_ROOT+"/"+del_track.track_image.name
                                if os.path.isfile(image_path):
                                    os.unlink(image_path)     

                            if(del_track.track_file):
                                    image_pathf = settings.MEDIA_ROOT+"/"+del_track.track_file.name
                                    if os.path.isfile(image_pathf):
                                        os.unlink(image_pathf)  

                        Tracks.objects.filter(pk=int(del_track.id)).delete()        

                    if(result_edit.album_image):
                        image_path = settings.MEDIA_ROOT+"/"+result_edit.album_image.name
                        if os.path.isfile(image_path):
                            os.unlink(image_path)  
                    
                    Album.objects.filter(pk=int(album_id)).delete()
                    c = Album.objects.filter(pk=int(album_id)).count()
                    if c:
                       messages.add_message(request, messages.ERROR, 'Not able to delete album!') 
                       return HttpResponseRedirect('/admin/album-details/'+result_edit.slug+'/')  
                    else:
                        mail_text = 'Album '+album_title+str(' deleted by admin')
                        edit_link = ""
                        content_email('Your Album Deleted',mail_text,edit_link,album_owner,request.session['admin_id'])
                        messages.add_message(request, messages.SUCCESS, 'Album deleted successfully!')
                        return HttpResponseRedirect('/admin/albums/')
                else:
                      messages.add_message(request, messages.ERROR, 'album not found!')
                      return HttpResponseRedirect('/admin/album-details/'+result_edit.slug+'/')
            
            elif 'btn_edit' in request.POST :  
                import re
                title=request.POST.get('title', "NONE")
                subtitle=request.POST.get('subtitle', "NONE")
                genre_id=request.POST.get('genre_id', "NONE")
                types_id=request.POST.get('types_id', "NONE")
                dedicate=request.POST.get('dedicate', "NONE")
                create_slug = title.lower()
                create_slug = create_slug.replace (" ", "-")
                create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
                if Album.objects.filter(slug=create_slug).exists():
                    _slugcheck=Album.objects.get(slug=create_slug)
                    if _slugcheck.id!=int(album_id):
                       count_slugs = Album.objects.filter(slug__contains=create_slug).count()
                       create_slug = create_slug+"-"+str(count_slugs)
                
                result_edit.title = title
                result_edit.slug = create_slug
                result_edit.subtitle = subtitle
                result_edit.genre_id=int(genre_id)
                result_edit.types_id=int(types_id)
                result_edit.dedicate = dedicate
                #result_edit.is_approved = 1
                result_edit.save()
                
                if len(request.FILES) != 0:
                    if 'album_image' in request.FILES:  
                        if(result_edit.album_image):
                            image_path = settings.MEDIA_ROOT+"/"+result_edit.album_image.name
                            if os.path.isfile(image_path):
                                os.unlink(image_path)                       
                        album_image = request.FILES['album_image']
                        result_edit.album_image = album_image
                        result_edit.save()
                
                mail_text = title+str(' edited by admin')
                edit_link = "http://"+request.get_host()+"/album-details/"+str(result_edit.slug)
                content_email('Your Album Edited',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
                messages.add_message(request, messages.SUCCESS, 'Album edited successfully!')
                return HttpResponseRedirect('/admin/album-details/'+result_edit.slug+'/')
                       
            else :
               print("Action not allowed") 
        else :
            print("this not a post method")
            
    else :
        return HttpResponseRedirect('/admin/login/')    
    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def album_delete(request):
    if request.method == 'POST':
        album_id=request.POST['album_id']
        if Album.objects.filter(pk=int(album_id)).exists():
            result_edit=Album.objects.get(pk=album_id)
            album_title = result_edit.title
            album_owner = result_edit.uploadby_id
            if Tracks.objects.filter(album_id=int(album_id)).exists():
                del_tracks=Tracks.objects.filter(album_id=int(album_id))
                for del_track in del_tracks:
                    if(del_track.track_image):
                        image_path = settings.MEDIA_ROOT+"/"+del_track.track_image.name
                        if os.path.isfile(image_path):
                            os.unlink(image_path)     

                    if(del_track.track_file):
                            image_pathf = settings.MEDIA_ROOT+"/"+del_track.track_file.name
                            if os.path.isfile(image_pathf):
                                os.unlink(image_pathf)  

                    Tracks.objects.filter(pk=int(del_track.id)).delete()        
            
            if(result_edit.album_image):
                image_path = settings.MEDIA_ROOT+"/"+result_edit.album_image.name
                if os.path.isfile(image_path):
                    os.unlink(image_path)         
            
            Album.objects.filter(pk=int(album_id)).delete()
            c = Album.objects.filter(pk=int(album_id)).count()
            if c:
                messages.add_message(request, messages.ERROR, 'Technical error!')
                return HttpResponse(0)
            else:
                mail_text = 'Album '+album_title+str(' deleted by admin')
                edit_link = ""
                content_email('Your Album Deleted',mail_text,edit_link,album_owner,request.session['admin_id'])
                messages.add_message(request, messages.SUCCESS, 'Album deleted successfully!')
                return HttpResponse(1)
        else:
            messages.add_message(request, messages.ERROR, 'Album not exists!')
            return HttpResponse(0)        
    
    else:
        messages.add_message(request, messages.ERROR, 'Not able to delete album!')
        return HttpResponse(0)
           
@cache_control(no_cache=True, must_revalidate=True, no_store=True)            
def album_approve(request):
    if request.method == 'POST':
        album_id=request.POST['album_id']
        result_edit=Album.objects.get(pk=album_id)
        result_edit.is_approved = 1
        result_edit.save()
        
        mail_text = 'Album '+result_edit.title+str(' is approved by admin')
        edit_link = "http://"+request.get_host()+"/album-details/"+str(result_edit.slug)
        content_email('Your Album Approved',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
        
        messages.add_message(request, messages.SUCCESS, 'Album status change to approve!') 
        return HttpResponse("1")
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def album_disapprove(request):
    if request.method == 'POST': 
        album_id=request.POST['album_id']
        result_edit=Album.objects.get(pk=album_id)
        result_edit.is_approved = 0
        result_edit.save()
        
        mail_text = 'Album '+result_edit.title+str(' is disapproved by admin')
        edit_link = "http://"+request.get_host()+"/album-details/"+str(result_edit.slug)
        content_email('Your Album Disapproved',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
        
        messages.add_message(request, messages.SUCCESS, 'Album status change to disapprove!') 
        return HttpResponse("1")    
        