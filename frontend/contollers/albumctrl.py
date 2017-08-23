from django.shortcuts import render
from django.template import context,Template,Context
from adminpanel.models import *
from frontend.contollers.commonctrl import *
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
import os
from django.conf import settings
from django.db import connection
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
            #album_image=request.FILES['album_image']
            album_image = None
            genre_id=request.POST.get('genre_id', "NONE")
            types_id=request.POST.get('types_id', "NONE")
            dedicate=request.POST.get('dedicate', "NONE")
            create_slug = title.lower()
            create_slug = create_slug.replace (" ", "-")
            create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
            
            if len(request.FILES) != 0:
                if 'album_image' in request.FILES:  
                    album_image = request.FILES['album_image']
            
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
def user_pending_albums(request):   
    if 'member_id' in request.session:
        pending_albums=Album.objects.filter(is_approved=0,uploadby_id=int(request.session['member_id']))
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
        return render(request,'frontend/pending-album-list.html',{'pending_albums':pending_albums })
    else :
        return HttpResponseRedirect('/')  
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def my_albums(request):   
    if 'member_id' in request.session:
        albums=Album.objects.filter(is_approved=1,uploadby_id=int(request.session['member_id']))
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
        return render(request,'frontend/albumlist.html',{'albums':albums })
    else :
        return HttpResponseRedirect('/')     
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def album_details(request,slug):    
    if 'member_id' in request.session:
        if Album.objects.filter(slug=slug,uploadby_id=int(request.session['member_id'])).exists():
            genre = get_genre()
            types = get_type()
            result=Album.objects.get(slug=slug)
            albumtracks=Tracks.objects.filter(album_id=result.id)
            return render(request,'frontend/album-detail.html',{'album':result, 'albumtracks':albumtracks ,'genre':genre, 'types' : types })
        else :
           messages.add_message(request, messages.ERROR, 'Not the right track!')  
           return HttpResponseRedirect('/dashboard/')  
    else :
        return HttpResponseRedirect('/') 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def public_album_details(request,slug):  
    if Album.objects.filter(slug=slug,is_approved=1).exists():
        result=Album.objects.get(slug=slug,is_approved=1)
        cursor = connection.cursor()
        
        cursor.execute("select usr.username as userslug, up.name as username from adminpanel_album as am INNER JOIN auth_user as usr ON usr.id = am.uploadby_id"
        " INNER JOIN adminpanel_userprofile as up ON up.user_id = am.uploadby_id where am.id ="+str(result.id))
        album_user=query_to_dicts(cursor)
        
        cursor.execute("select usr.username as userslug, up.name as username, ag.title as genretitle, am.* from adminpanel_genre as ag INNER JOIN adminpanel_album as am ON ag.id = am.genre_id"
        " INNER JOIN auth_user as usr ON usr.id = am.uploadby_id"
        " INNER JOIN adminpanel_userprofile as up ON up.user_id = am.uploadby_id where am.genre_id = "+str(result.genre_id)+" and am.is_approved = 1 and am.id <>"+str(result.id)+" ORDER BY am.id DESC" )
        related_albums = dictfetchall(cursor)
        return render(request,'frontend/public-album-detail.html',{'album':result, 'related_albums':related_albums, 'album_user':album_user })
    else :
        messages.add_message(request, messages.ERROR, 'Not the right track!')  
        return HttpResponseRedirect('/dashboard/') 
       
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def public_album_tracks(request):
    if request.POST:
        resultarr = []
        album_id=request.POST.get('album_id', "NONE")
        albumtracks=Tracks.objects.filter(album_id=album_id)
        import json
        count = 0
        for albumtrack in albumtracks:
            count += 1
            res_json = {}
            res_json['track_id'] = albumtrack.id
            res_json['name'] = albumtrack.title
            res_json['file'] = albumtrack.track_file.name
            res_json['track'] = count
            resultarr.append(res_json)
        data = json.dumps(resultarr)
        return HttpResponse(data)
    else:
        return HttpResponse(0)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def album_edit(request):
    if 'member_id' in request.session:
        if request.method == 'POST':
            album_id=request.POST['album_id']
            result_edit=Album.objects.get(pk=album_id)
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
                       return HttpResponseRedirect('/album-details/'+result_edit.slug+'/')  
                    else:
                        messages.add_message(request, messages.SUCCESS, 'Album deleted successfully!')
                        return HttpResponseRedirect('/my-albums/')
                else:
                      messages.add_message(request, messages.ERROR, 'Not able to delete album!')
                      return HttpResponseRedirect('/album-details/'+result_edit.slug+'/')
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
                result_edit.is_approved = 1
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
                '''   
                admininfo = ns_get_user(1)
                edit_link = "http://"+request.get_host()+"/admin/track-details/"+str(result_edit.slug)
                approval_track_mail=EmailTemplates.objects.get(pk=6) 
                t = Template(approval_track_mail.templatebody)
                c = Context({'approval_text' : 'Track Approval','edit_link' : edit_link })
                msg_html = t.render(c)
                send_mail(approval_track_mail.subject, 'hello world again', admininfo.email, [admininfo.email], html_message=msg_html)
                '''
                messages.add_message(request, messages.SUCCESS, 'Album edited successfully!')
                return HttpResponseRedirect('/album-details/'+result_edit.slug+'/')
                       
            else :
               print("Action not allowed") 
        else :
            print("this not a post method")
            
    else :
        return HttpResponseRedirect('/')    
        