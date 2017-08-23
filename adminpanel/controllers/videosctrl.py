from django.shortcuts import render
from django.template import context
from adminpanel.models import *
from adminpanel.controllers.commonctrl import *
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_control
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload_videos(request):
    if 'admin_id' in request.session:
        genre = get_genre()
        types = get_type()
        if request.method == 'POST':
            import re
            title=request.POST.get('title', "NONE")
            subtitle=request.POST.get('subtitle', "NONE")
            link=request.POST.get('link', "NONE")
            embedlink = link.replace('watch?v=','embed/')
            artist_name=request.POST.get('artist_name', "NONE")
            genre_id=request.POST.get('genre_id', "NONE")
            types_id=request.POST.get('types_id', "NONE")
            dedicate=request.POST.get('dedicate', "NONE")
            create_slug = title.lower()
            create_slug = create_slug.replace (" ", "-")
            create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
            
            if Video.objects.filter(slug=create_slug).exists():
                count_slugs = Video.objects.filter(slug__contains=create_slug).count()
                create_slug = create_slug+"-"+str(count_slugs)
            
            add_video = Video(
                title=title,
                slug=create_slug,
                subtitle=subtitle,
                link=embedlink,
                link_url=link,
                artist=artist_name,
                genre_id=int(genre_id),
                types_id=int(types_id),
                dedicate=dedicate,
                uploadby_id=int(request.session['member_id']),
                is_approved=0
            )
            add_video.save()
            messages.add_message(request, messages.SUCCESS, 'Video uploaded waiting for approval!') 
            return HttpResponseRedirect('/pending-videos/')    
        return render(request,'frontend/videoupload.html',{'genre':genre,'types':types})
    else :
        return HttpResponseRedirect('/')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_pending_videos(request,userid,likes_order=None):    
    if 'admin_id' in request.session:
        result=pending_videos(request,userid,likes_order)
        return render(request,'adminpanel/pending-videos.html',{'pending_videos':result,'user_id':userid,'likes_order':likes_order })
    else :
        return HttpResponseRedirect('/')  
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_pending_videos(request,likes_order=None):
    if 'admin_id' in request.session:
        result=pending_videos(request,"",likes_order)
        return render(request,'adminpanel/pending-videos.html',{'pending_videos':result,'user_id':None,'likes_order':likes_order })
    else :
        return HttpResponseRedirect('/')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_videos(request,userid,likes_order=None):    
    if 'admin_id' in request.session:
        result=videos(request,userid,likes_order)
        return render(request,'adminpanel/video-listing.html',{'videos':result,'user_id':userid,'likes_order':likes_order })
    else :
        return HttpResponseRedirect('/')  
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_videos(request,likes_order=None):
    if 'admin_id' in request.session:
        result=videos(request,"",likes_order)
        return render(request,'adminpanel/video-listing.html',{'videos':result,'user_id':None,'likes_order':likes_order })
    else :
        return HttpResponseRedirect('/')    
    

def pending_videos(request,userid,likes_order=None):   
        if userid:
            if likes_order == "asc":
                pending_videos=Video.objects.filter(is_approved=0,uploadby_id=userid).order_by('like_counts')
            elif likes_order == "desc" :
                pending_videos=Video.objects.filter(is_approved=0,uploadby_id=userid).order_by('-like_counts')
            else :
               pending_videos=Video.objects.filter(is_approved=0,uploadby_id=userid) 
        else:
            if likes_order == "asc":
                pending_videos=Video.objects.filter(is_approved=0).order_by('like_counts')
            elif likes_order == "desc" :    
                pending_videos=Video.objects.filter(is_approved=0).order_by('like_counts')
            else :
               pending_videos=Video.objects.filter(is_approved=0) 
        paginator = Paginator(pending_videos, 12) # Show 10 contacts per page
        page = request.GET.get('page')
        try:
            pending_videos = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pending_videos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            pending_videos = paginator.page(paginator.num_pages)
        return pending_videos
      


def videos(request,userid,likes_order):   
        if userid:
            if likes_order == "asc":
                videos=Video.objects.filter(is_approved=1,uploadby_id=userid).order_by('like_counts')
            elif likes_order == "desc" :
                videos=Video.objects.filter(is_approved=1,uploadby_id=userid).order_by('-like_counts')
            else:
               videos=Video.objects.filter(is_approved=1,uploadby_id=userid) 
        else : 
            if likes_order == "asc":
                videos=Video.objects.filter(is_approved=1).order_by('like_counts')
            elif likes_order == "desc" :
                videos=Video.objects.filter(is_approved=1).order_by('-like_counts') 
            else :
                videos=Video.objects.filter(is_approved=1)  
        paginator = Paginator(videos, 12) # Show 10 contacts per page
        page = request.GET.get('page')
        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            videos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            videos = paginator.page(paginator.num_pages)
        return videos
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def video_details(request,slug):    
    if 'admin_id' in request.session:
        if Video.objects.filter(slug=slug).exists():
            genre = get_genre()
            types = get_type()
            result=Video.objects.get(slug=slug)
            return render(request,'adminpanel/video-detail.html',{'video':result, 'genre':genre, 'types' : types })
        else :
           return HttpResponseRedirect('/admin/artists/')  
    else :
        return HttpResponseRedirect('/') 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def video_edit(request):
    if 'admin_id' in request.session:
        if request.method == 'POST':
            video_id=request.POST['video_id']
            result_edit=Video.objects.get(pk=video_id)
            video_title = result_edit.title
            if 'btn_delete' in request.POST :  
                if Video.objects.filter(pk=int(video_id)).exists():
                   Video.objects.filter(pk=int(video_id)).delete()
                   c = Video.objects.filter(pk=int(video_id)).count()
                   if c:
                      messages.add_message(request, messages.ERROR, 'Not able to delete video!') 
                      return HttpResponseRedirect('/admin/video-details/'+result_edit.slug+'/')  
                   else:
                       mail_text = video_title+str(' is deleted by admin')
                       edit_link = ""
                       content_email('Your Video Deleted',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
                       messages.add_message(request, messages.SUCCESS, 'Video deleted successfully!')
                       return HttpResponseRedirect('/admin/videos/')
                else:
                      messages.add_message(request, messages.ERROR, 'Not able to delete video!')
                      return HttpResponseRedirect('/admin/video-details/'+result_edit.slug+'/')
            elif 'btn_disapprove' in request.POST :  
                result_edit.is_approved = 0
                result_edit.save()
                
                mail_text = 'Video '+result_edit.title+str(' is disapproved by admin')
                edit_link = "http://"+request.get_host()+"/video-details/"+str(result_edit.slug)
                content_email('Your Album Disapproved',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
                
                messages.add_message(request, messages.SUCCESS, 'video status change to disapprove!') 
                return HttpResponseRedirect('/admin/video-details/'+result_edit.slug+'/')
            elif 'btn_approve' in request.POST :  
                result_edit.is_approved = 1
                result_edit.save()
                
                mail_text = 'Video '+result_edit.title+str(' is approved by admin')
                edit_link = "http://"+request.get_host()+"/video-details/"+str(result_edit.slug)
                content_email('Your Album Approved',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
                
                messages.add_message(request, messages.SUCCESS, 'video status change to approve')
                return HttpResponseRedirect('/admin/video-details/'+result_edit.slug+'/')
            elif 'btn_edit' in request.POST :  
                import re
                title=request.POST.get('title', "NONE")
                subtitle=request.POST.get('subtitle', "NONE")
                link=request.POST.get('link', "NONE")
                embedlink = link.replace('watch?v=','embed/')
                #artist_name=request.POST.get('artist_name', "NONE")
                genre_id=request.POST.get('genre_id', "NONE")
                types_id=request.POST.get('types_id', "NONE")
                dedicate=request.POST.get('dedicate', "NONE")
                
                create_slug = title.lower()
                create_slug = create_slug.replace (" ", "-")
                create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
                if Video.objects.filter(slug=create_slug).exists():
                    _slugcheck=Video.objects.get(slug=create_slug)
                    if _slugcheck.id!=int(video_id):
                       count_slugs = Video.objects.filter(slug__contains=create_slug).count()
                       create_slug = create_slug+"-"+str(count_slugs)
                
                result_edit.title = title
                result_edit.slug = create_slug
                result_edit.subtitle = subtitle
                result_edit.link = embedlink
                result_edit.link_url = link
                result_edit.genre_id = genre_id
                result_edit.types_id = types_id
                result_edit.dedicate = dedicate
                result_edit.save()
                
                mail_text = 'Video '+result_edit.title+str(' is edited by admin')
                edit_link = "http://"+request.get_host()+"/video-details/"+str(result_edit.slug)
                content_email('Your Album Edited',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
                
                messages.add_message(request, messages.SUCCESS, 'video edited successfully!')
                return HttpResponseRedirect('/admin/video-details/'+result_edit.slug+'/')
                       
            else :
               print("Action not allowed") 
        else :
            print("this not a post method")
            
    else :
        return HttpResponseRedirect('/')   
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def video_delete(request):
    if request.method == 'POST':
        video_id=request.POST['video_id']
        result_edit=Video.objects.get(pk=video_id)
        video_title = result_edit.title
        if Video.objects.filter(pk=int(video_id)).exists():
            Video.objects.filter(pk=int(video_id)).delete()
            c = Video.objects.filter(pk=int(video_id)).count()
            if c:
                messages.add_message(request, messages.ERROR, 'Technical error!')
                return HttpResponse(0)
            else:
                mail_text = video_title+str(' is deleted by admin')
                edit_link = ""
                content_email('Your Video Deleted',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
                messages.add_message(request, messages.SUCCESS, 'Video deleted successfully!')
                return HttpResponse(0)
        else:
            messages.add_message(request, messages.ERROR, 'Not able to delete video!')
            return HttpResponse(0)
           
            
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def video_approve(request):
    if request.method == 'POST':
        video_id=request.POST['video_id']
        result_edit=Video.objects.get(pk=video_id)
        result_edit.is_approved = 1
        result_edit.save()
        
        mail_text = 'Video '+result_edit.title+str(' is approved by admin')
        edit_link = "http://"+request.get_host()+"/video-details/"+str(result_edit.slug)
        content_email('Your Album Approved',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
        
        messages.add_message(request, messages.SUCCESS, 'Video status change to approve!') 
        return HttpResponse("1")
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def video_disapprove(request):
    if request.method == 'POST': 
        video_id=request.POST['video_id']
        result_edit=Video.objects.get(pk=video_id)
        result_edit.is_approved = 0
        result_edit.save()
        
        mail_text = 'Video '+result_edit.title+str(' is disapproved by admin')
        edit_link = "http://"+request.get_host()+"/video-details/"+str(result_edit.slug)
        content_email('Your Album Disapproved',mail_text,edit_link,result_edit.uploadby_id,request.session['admin_id'])
        
        messages.add_message(request, messages.SUCCESS, 'Video status change to disapprove!') 
        return HttpResponse("1")    
        
         
        