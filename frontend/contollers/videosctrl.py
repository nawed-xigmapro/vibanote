from django.shortcuts import render
from django.template import context,Template,Context
from adminpanel.models import *
from frontend.contollers.commonctrl import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.cache import cache_control
from django.db import connection
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload_videos(request):
    if 'member_id' in request.session:
        genre = get_genre()
        types = get_type()
        if request.method == 'POST':
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
                count_slugs = Video.objects.filter(slug__contains=create_slug).count()
                create_slug = create_slug+"-"+str(count_slugs)
            
            add_video = Video(
                title=title,
                slug=create_slug,
                subtitle=subtitle,
                link=embedlink,
                link_url=link,
                genre_id=int(genre_id),
                types_id=int(types_id),
                dedicate=dedicate,
                uploadby_id=int(request.session['member_id']),
                is_approved=0
            )
            add_video.save()
            admininfo = ns_get_user(1)
            edit_link = "http://"+request.get_host()+"/admin/video-details/"+str(add_video.slug)
            approval_video_mail=EmailTemplates.objects.get(pk=6) 
            t = Template(approval_video_mail.templatebody)
            c = Context({'approval_text' : 'Video Approval' ,'edit_link' : edit_link })
            msg_html = t.render(c)
            send_mail(approval_video_mail.subject, 'hello world again', admininfo.email, [admininfo.email], html_message=msg_html)
            
            messages.add_message(request, messages.SUCCESS, 'Video uploaded waiting for approval!') 
            return HttpResponseRedirect('/pending-videos/')    
        return render(request,'frontend/videoupload.html',{'genre':genre,'types':types})
    else :
        return HttpResponseRedirect('/')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pending_videos(request):   
    if 'member_id' in request.session:
        pending_videos=Video.objects.filter(is_approved=0,uploadby_id=int(request.session['member_id']))
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
        return render(request,'frontend/pending-videos.html',{'pending_videos':pending_videos })
    else :
        return HttpResponseRedirect('/')  
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def my_videos(request):   
    if 'member_id' in request.session:
        videos=Video.objects.filter(is_approved=1,uploadby_id=int(request.session['member_id']))
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
        return render(request,'frontend/video-listing.html',{'videos':videos })
    else :
        return HttpResponseRedirect('/')     
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def video_details(request,slug):    
    if 'member_id' in request.session:
        if Video.objects.filter(slug=slug,uploadby_id=int(request.session['member_id'])).exists():
            genre = get_genre()
            types = get_type()
            result=Video.objects.get(slug=slug)
            return render(request,'frontend/video-detail.html',{'video':result, 'genre':genre, 'types' : types })
        else :
           messages.add_message(request, messages.ERROR, 'Not the right video!')  
           return HttpResponseRedirect('/dashboard/')  
    else :
        return HttpResponseRedirect('/') 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def video_edit(request):
    if 'member_id' in request.session:
        if request.method == 'POST':
            video_id=request.POST['video_id']
            result_edit=Video.objects.get(pk=video_id)
            if 'btn_delete' in request.POST :  
                if Video.objects.filter(pk=int(video_id)).exists():
                   Video.objects.filter(pk=int(video_id)).delete()
                   c = Video.objects.filter(pk=int(video_id)).count()
                   if c:
                      messages.add_message(request, messages.ERROR, 'Not able to delete video!') 
                      return HttpResponseRedirect('/video-details/'+result_edit.slug+'/')  
                   else:
                       messages.add_message(request, messages.SUCCESS, 'Video deleted successfully!')
                       return HttpResponseRedirect('/my-videos/')
                else:
                      messages.add_message(request, messages.ERROR, 'Not able to delete video!')
                      return HttpResponseRedirect('/video-details/'+result_edit.slug+'/')
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
                result_edit.is_approved = 0
                result_edit.save()
                admininfo = ns_get_user(1)
                edit_link = "http://"+request.get_host()+"/admin/video-details/"+str(result_edit.slug)
                approval_video_mail=EmailTemplates.objects.get(pk=6) 
                t = Template(approval_video_mail.templatebody)
                c = Context({ 'edit_link' : edit_link })
                msg_html = t.render(c)
                send_mail(approval_video_mail.subject, 'hello world again', admininfo.email, [admininfo.email], html_message=msg_html)
                
                messages.add_message(request, messages.SUCCESS, 'video edited successfully waiting for approval!')
                return HttpResponseRedirect('/video-details/'+result_edit.slug+'/')
                       
            else :
               print("Action not allowed") 
        else :
            print("this not a post method")
            
    else :
        return HttpResponseRedirect('/')    
    
def public_video_detail(request,videoslug):   
    if Video.objects.filter(slug=videoslug,is_approved=1).exists(): 
        cursor = connection.cursor()
        cursor.execute("select au.username,up.name,up.user_id,up.picture,av.*,ag.title as genretitle,atyp.title as typetitle from adminpanel_video as av INNER JOIN adminpanel_userprofile as up on up.user_id=av.uploadby_id"
        " INNER JOIN auth_user as au  ON au.id = up.user_id" 
        " INNER JOIN adminpanel_genre as ag  ON av.genre_id = ag.id" 
        " INNER JOIN adminpanel_type as atyp  ON av.genre_id = atyp.id" 
        " where av.is_approved=1 and av.slug = '"+str(videoslug)+"'")  
        video_details=query_to_dicts(cursor)
        return render(request,'frontend/public_video_detail.html',{'video_details':video_details})     
    else:
       messages.add_message(request, messages.ERROR, 'video not found!') 
       return HttpResponseRedirect('/')     
        