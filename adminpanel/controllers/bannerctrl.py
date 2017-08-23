from django.template import context
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db import connection
from django.utils import formats
from adminpanel.models import *
import os
from django.conf import settings
from django.views.decorators.cache import cache_control

# Create your views here.
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def list_banner(request):
   if 'admin_id' in request.session:
        return render(request, 'adminpanel/list-banner.html')
   else :
       return HttpResponseRedirect('/admin/login/')

def get_allbanner(request):
        totalrows = Banner.objects.count()
        cursor = connection.cursor()
        order = request.GET['order']

        if 'search' in request.GET and 'sort' not in request.GET :
         column_name = 'adminpanel_banner.title'
         srch = request.GET['search']
         cursor.execute("select * from adminpanel_banner where adminpanel_banner.title like '"+srch+"%' or adminpanel_banner.subtitle like '"+srch+"%' ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' in request.GET :
            srch = request.GET['search']
            sort = request.GET['sort']
            if sort == "title":
                column_name = 'adminpanel_banner.title'
            elif sort == "subtitle":
                column_name = 'adminpanel_banner.subtitle'
            else :
             column_name = 'adminpanel_banner.id'

            if srch :
              cursor.execute("select * from adminpanel_banner where adminpanel_banner.title like '"+srch+"%' or adminpanel_banner.subtitle like '"+srch+"%' ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])
            else:
             cursor.execute("select * from adminpanel_banner ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' not in request.GET:
            sort = request.GET['sort']
            if sort == "title":
                column_name = 'adminpanel_banner.title'
            elif sort == "subtitle":
                column_name = 'adminpanel_banner.subtitle'
            else :
             column_name = 'adminpanel_banner.id'

            cursor.execute("select * from adminpanel_banner ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        else :
         column_name = 'adminpanel_banner.id'
         cursor.execute("select * from adminpanel_banner ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        all_banner = dictfetchall(cursor)
        docs_dict = {
            'total': totalrows,
            'rows': [{'id': all_ban['id'],
                      'title': all_ban['title'],
                      'created_date': formats.date_format(all_ban['created_date'], "Y-m-d"),
                      'subtitle': all_ban['subtitle'],
                      'details': all_ban['id'],
                      } for all_ban in all_banner]
        }
        return JsonResponse(docs_dict)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_banner(request):
   if 'admin_id' in request.session:
       title =""
       content=""
       if request.POST:
            import re
            title = request.POST.get('title',None)
            subtitle = request.POST.get('subtitle',None)
            content = request.POST.get('content',None)
            picture = None
            create_slug = title.lower()
            create_slug = create_slug.replace (" ", "-")
            create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
            
            if Banner.objects.filter(slug=create_slug).exists():
                count_slugs = Banner.objects.filter(slug__contains=create_slug).count()
                create_slug = create_slug+"-"+str(count_slugs)
            
            if len(request.FILES) != 0:
                picture = request.FILES['picture']
                create_banner = Banner(
                             title=title,
                             subtitle=subtitle,
                             slug=create_slug,
                             text = content,
                             picture = picture,
                             author_id = request.session['admin_id']
                             )
                create_banner.save()
            else:
                create_banner = Banner(
                             title=title,
                             subtitle=subtitle,
                             slug=create_slug,
                             text = content,
                             author_id = request.session['admin_id']
                             )
                create_banner.save()
            
            return HttpResponseRedirect('/admin/banner/')


       #return render_to_response('adminpanel/create_banner.html', {'title': title, 'slug': slug, 'content': content } , context_instance = RequestContext(request))
       return render(request, 'adminpanel/add-banner.html',{})
   else :
       return HttpResponseRedirect('/admin/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def banner_details(request,banner_id):
   if 'admin_id' in request.session:
             if banner_id :
                         if Banner.objects.filter(pk=banner_id).exists():
                               banner_edit=Banner.objects.get(pk=banner_id)
                         else :
                           return HttpResponseRedirect('/admin/banner/')
             else :
                  return HttpResponseRedirect('/admin/banner/')


             #return render_to_response('adminpanel/edit_Banner.html',{'title': title, 'slug': slug, 'content': content, 'banner_id' : banner_id } ,context_instance = RequestContext(request))
             return render(request, 'adminpanel/edit-banner.html',{"banner":banner_edit})
   else :
       return HttpResponseRedirect('/admin/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_banner(request):
    if request.method == 'POST' and 'btn_edit' in request.POST :
       import re
       banner_id = request.POST.get('banner_id','NONE')
       title = request.POST.get('title','NONE')
       #subtitle = request.POST.get('subtitle','NONE')
       #content = request.POST.get('content','NONE')

       create_slug = title.lower()
       create_slug = create_slug.replace (" ", "-")
       create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
       
       if Banner.objects.filter(slug=create_slug).exists():
            slugcheck=Banner.objects.get(slug=create_slug)
            if slugcheck.id!=int(banner_id):
               count_slugs = Banner.objects.filter(slug__contains=create_slug).count()
               create_slug = create_slug+"-"+str(count_slugs)
       
                
       banner_edit=Banner.objects.get(pk=int(banner_id))
       banner_edit.title=title
       banner_edit.slug=create_slug
       #banner_edit.text = content
       #banner_edit.subtitle = subtitle
       banner_edit.save()
       
       if len(request.FILES) != 0:
            if banner_edit.picture:
                image_path = settings.MEDIA_ROOT+"/"+banner_edit.picture.name
                os.unlink(image_path)
            picture = request.FILES['picture']
            banner_edit.picture = picture
            banner_edit.save()
       return HttpResponseRedirect('/admin/banner-details/'+banner_id+'/')
    
    elif request.method == 'POST' and 'btn_delete' in request.POST :
        delete_id = request.POST.get('banner_id','NONE')
        res = delete_Banner(delete_id)
        if res == 1 :
            return HttpResponseRedirect('/admin/login/') 
        else :
            return HttpResponseRedirect('/admin/banner/') 
    else :
       return HttpResponseRedirect('/admin/login/')    

def delete_banner(delete_id):
    if Banner.objects.filter(pk=int(delete_id)).exists():
        banner_delete = Banner.objects.get(pk=int(delete_id))
        if len(request.FILES) != 0:
            if banner_delete.picture:
                image_path = settings.MEDIA_ROOT+"/"+banner_edit.picture.name
                os.unlink(image_path)
        Banner.objects.filter(pk=int(delete_id)).delete()
        c = Banner.objects.filter(pk=int(delete_id)).count()
        if c:
           return 1   
        else:
            return 0
    else:
           return 1  
       
