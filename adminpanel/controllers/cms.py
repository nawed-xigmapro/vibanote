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
def list_cms(request):
   if 'admin_id' in request.session:
        #return render_to_response('adminpanel/list_cms.html', context_instance = RequestContext(request))
        return render(request, 'adminpanel/list_cms.html')
   else :
       return HttpResponseRedirect('/admin/login/')

def get_allcms(request):
        totalrows = Cms.objects.count()
        cursor = connection.cursor()
        order = request.GET['order']

        if 'search' in request.GET and 'sort' not in request.GET :
         column_name = 'adminpanel_cms.title'
         srch = request.GET['search']
         cursor.execute("select * from adminpanel_cms where adminpanel_cms.title like '"+srch+"%' ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' in request.GET :
            srch = request.GET['search']
            sort = request.GET['sort']
            if sort == "cms_title":
                column_name = 'adminpanel_cms.title'
            elif sort == "cms_slug":
                column_name = 'adminpanel_cms.slug'
            else :
             column_name = 'adminpanel_cms.id'

            if srch :
              cursor.execute("select * from adminpanel_cms where adminpanel_cms.title like '"+srch+"%' ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])
            else:
             cursor.execute("select * from adminpanel_cms ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' not in request.GET:
            sort = request.GET['sort']
            if sort == "cms_title":
                column_name = 'adminpanel_cms.title'
            elif sort == "cms_slug":
                column_name = 'adminpanel_cms.slug'
            else :
             column_name = 'adminpanel_cms.id'

            cursor.execute("select * from adminpanel_cms ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        else :
         column_name = 'adminpanel_cms.id'
         cursor.execute("select * from adminpanel_cms ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        all_cms = dictfetchall(cursor)
        docs_dict = {
            'total': totalrows,
            'rows': [{'id': all_cm['id'],
                      'cms_title': all_cm['title'],
                      'cms_startdate': formats.date_format(all_cm['created_date'], "Y-m-d"),
                      'cms_slug': all_cm['slug'],
                      'cms_details': all_cm['id'],
                      } for all_cm in all_cms]
        }
        return JsonResponse(docs_dict)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_cms(request):
   if 'admin_id' in request.session:
       cms_title =""
       cms_content=""
       if request.POST:
            import re
            cms_title = request.POST.get('cms_title','NONE')
            cms_content = request.POST.get('cms_content','NONE')
            cms_pic = None
            create_slug = cms_title.lower()
            create_slug = create_slug.replace (" ", "-")
            create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
            
            if Cms.objects.filter(slug=create_slug).exists():
                count_slugs = Cms.objects.filter(slug__contains=create_slug).count()
                create_slug = create_slug+"-"+str(count_slugs)
            
            if len(request.FILES) != 0:
                cms_pic = request.FILES['picture']
                create_cms = Cms(
                             title=cms_title,
                             slug=create_slug,
                             text = cms_content,
                             picture = cms_pic,
                             author_id = request.session['admin_id']
                             )
                create_cms.save()
            else:
                create_cms = Cms(
                             title=cms_title,
                             slug=create_slug,
                             text = cms_content,
                             author_id = request.session['admin_id']
                             )
                create_cms.save()
            
            return HttpResponseRedirect('/admin/cms/')


       #return render_to_response('adminpanel/create_cms.html', {'cms_title': cms_title, 'cms_slug': cms_slug, 'cms_content': cms_content } , _instance = RequestContext(request))
       return render(request, 'adminpanel/create_cms.html',{'cms_title': cms_title, 'cms_content': cms_content })
   else :
       return HttpResponseRedirect('/admin/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cms_details(request,cms_id):
   if 'admin_id' in request.session:
             if cms_id :
                         if Cms.objects.filter(pk=cms_id).exists():
                               cms_edit=Cms.objects.get(pk=cms_id)
                               cms_title = cms_edit.title
                               cms_content = cms_edit.text
                               cms_pic = cms_edit.picture
                         else :
                           return HttpResponseRedirect('/admin/cms/')
             else :
                  return HttpResponseRedirect('/admin/cms/')


             #return render_to_response('adminpanel/edit_cms.html',{'cms_title': cms_title, 'cms_slug': cms_slug, 'cms_content': cms_content, 'cms_id' : cms_id } ,context_instance = RequestContext(request))
             return render(request, 'adminpanel/edit_cms.html',{'cms_title': cms_title, 'cms_content': cms_content, 'cms_id' : cms_id, 'cms_pic' : cms_pic })
   else :
       return HttpResponseRedirect('/admin/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_cms(request):
    if request.method == 'POST' and 'btn_edit' in request.POST :
       import re
       cms_id = request.POST.get('cms_id','NONE')
       cms_title = request.POST.get('cms_title','NONE')
       #cms_slug = request.POST.get('cms_slug','NONE')
       cms_content = request.POST.get('cms_content','NONE')

       create_slug = cms_title.lower()
       create_slug = create_slug.replace (" ", "-")
       create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
       
       if Cms.objects.filter(slug=create_slug).exists():
            cms_slugcheck=Cms.objects.get(slug=create_slug)
            if cms_slugcheck.id!=int(cms_id):
               count_slugs = Cms.objects.filter(slug__contains=create_slug).count()
               create_slug = create_slug+"-"+str(count_slugs)
       
                
       cms_edit=Cms.objects.get(pk=int(cms_id))
       cms_edit.title=cms_title
       cms_edit.slug=create_slug
       cms_edit.text = cms_content
       cms_edit.save()
       
       if len(request.FILES) != 0:
            if cms_edit.picture:
                image_path = settings.MEDIA_ROOT+"/"+cms_edit.picture.name
                os.unlink(image_path)
            cms_pic = request.FILES['picture']
            cms_edit.picture = cms_pic
            cms_edit.save()
       return HttpResponseRedirect('/admin/cms-details/'+cms_id+'/')
    
    elif request.method == 'POST' and 'btn_delete' in request.POST :
        delete_id = request.POST.get('cms_id','NONE')
        res = delete_cms(delete_id)
        if res == 1 :
            return HttpResponseRedirect('/admin/login/') 
        else :
            return HttpResponseRedirect('/admin/cms/') 
    else :
       return HttpResponseRedirect('/admin/login/')    

def delete_cms(delete_id):
    if Cms.objects.filter(pk=int(delete_id)).exists():
        Cms.objects.filter(pk=int(delete_id)).delete()
        c = Cms.objects.filter(pk=int(delete_id)).count()
        if c:
           return 1   
        else:
            return 0
    else:
           return 1  
       
