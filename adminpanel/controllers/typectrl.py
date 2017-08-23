from django.template import context
from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from django.db import connection
from django.utils import formats
from adminpanel.models import Type
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
def list_type(request):
   if 'admin_id' in request.session:
        return render(request, 'adminpanel/list_type.html')
   else :
       return HttpResponseRedirect('/admin/login/')

def get_alltype(request):
        totalrows = Type.objects.count()
        cursor = connection.cursor()
        order = request.GET['order']

        if 'search' in request.GET and 'sort' not in request.GET :
         column_name = 'adminpanel_type.title'
         srch = request.GET['search']
         cursor.execute("select * from adminpanel_type where adminpanel_type.title like '"+srch+"%' ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' in request.GET :
            srch = request.GET['search']
            sort = request.GET['sort']
            if sort == "title":
                column_name = 'adminpanel_type.title'
            elif sort == "slug":
                column_name = 'adminpanel_type.slug'
            else :
             column_name = 'adminpanel_type.id'

            if srch :
              cursor.execute("select * from adminpanel_type where adminpanel_type.title like '"+srch+"%' ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])
            else:
             cursor.execute("select * from adminpanel_type ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' not in request.GET:
            sort = request.GET['sort']
            if sort == "title":
                column_name = 'adminpanel_type.title'
            elif sort == "slug":
                column_name = 'adminpanel_type.slug'
            else :
             column_name = 'adminpanel_type.id'

            cursor.execute("select * from adminpanel_type ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        else :
         column_name = 'adminpanel_type.id'
         cursor.execute("select * from adminpanel_type ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        all_types = dictfetchall(cursor)
        docs_dict = {
            'total': totalrows,
            'rows': [{'id': all_type['id'],
                      'title': all_type['title'],
                      'createdate': formats.date_format(all_type['created_date'], "Y-m-d"),
                      'details': all_type['id'],
                     } for all_type in all_types]
        }
        return JsonResponse(docs_dict)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_type(request):
    if 'admin_id' in request.session:
       
        if request.POST:
            import re
            title = request.POST.get('text','NONE')
            text = request.POST.get('text','NONE')
            create_slug = title.lower()
            create_slug = create_slug.replace (" ", "-")
            create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
            
            if Type.objects.filter(slug=create_slug).exists():
                count_slugs = Type.objects.filter(slug__contains=create_slug).count()
                create_slug = create_slug+"-"+str(count_slugs)
            
            addtype = Type(
                title=title,
                slug=create_slug,
                text = text,
            )
            addtype.save()
            
            return HttpResponseRedirect('/admin/types/')

        return render(request, 'adminpanel/add_type.html',{})
    else :
       return HttpResponseRedirect('/admin/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def type_details(request,id):
    if 'admin_id' in request.session:
            if id :
                if Type.objects.filter(pk=id).exists():
                    typedetails=Type.objects.get(pk=id)
                else :
                    return HttpResponseRedirect('/admin/types/')
            else :
                return HttpResponseRedirect('/admin/types/')

            return render(request, 'adminpanel/edit_type.html',{'typedetails': typedetails })
    else :
       return HttpResponseRedirect('/admin/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_type(request):
    if request.method == 'POST' and 'btn_edit' in request.POST :
       import re
       type_id = request.POST.get('type_id','NONE')
       title = request.POST.get('title','NONE')
       text = request.POST.get('text','NONE')

       create_slug = title.lower()
       create_slug = create_slug.replace (" ", "-")
       create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
       
       if Type.objects.filter(slug=create_slug).exists():
            type_slugcheck=Type.objects.get(slug=create_slug)
            if type_slugcheck.id!=int(type_id):
               count_slugs = Type.objects.filter(slug__contains=create_slug).count()
               create_slug = create_slug+"-"+str(count_slugs)
       
                
       type_edit=Type.objects.get(pk=int(type_id))
       type_edit.title=title
       type_edit.slug=create_slug
       type_edit.text = text
       type_edit.save()
       
       
       return HttpResponseRedirect('/admin/type-details/'+type_id+'/')
    
    elif request.method == 'POST' and 'btn_delete' in request.POST :
        type_id = request.POST.get('type_id','NONE')
        res = delete_type(type_id)
        if res == 1 :
            return HttpResponseRedirect('/admin/login/') 
        else :
            return HttpResponseRedirect('/admin/types/') 
    else :
       return HttpResponseRedirect('/admin/login/')    

def delete_type(delete_id):
    if Type.objects.filter(pk=int(delete_id)).exists():
        Type.objects.filter(pk=int(delete_id)).delete()
        c = Type.objects.filter(pk=int(delete_id)).count()
        if c:
           return 1   
        else:
            return 0
    else:
           return 1  
       
