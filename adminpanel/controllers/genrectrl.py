from django.template import context
from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from django.db import connection
from django.utils import formats
from adminpanel.models import Genre
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
def list_genre(request):
   if 'admin_id' in request.session:
        return render(request, 'adminpanel/list_genre.html')
   else :
       return HttpResponseRedirect('/admin/login/')

def get_allgenre(request):
        totalrows = Genre.objects.count()
        cursor = connection.cursor()
        order = request.GET['order']

        if 'search' in request.GET and 'sort' not in request.GET :
         column_name = 'adminpanel_genre.title'
         srch = request.GET['search']
         cursor.execute("select * from adminpanel_genre where adminpanel_genre.title like '"+srch+"%' ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' in request.GET :
            srch = request.GET['search']
            sort = request.GET['sort']
            if sort == "title":
                column_name = 'adminpanel_genre.title'
            elif sort == "slug":
                column_name = 'adminpanel_genre.slug'
            else :
             column_name = 'adminpanel_genre.id'

            if srch :
              cursor.execute("select * from adminpanel_genre where adminpanel_genre.title like '"+srch+"%' ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])
            else:
             cursor.execute("select * from adminpanel_genre ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' not in request.GET:
            sort = request.GET['sort']
            if sort == "title":
                column_name = 'adminpanel_genre.title'
            elif sort == "slug":
                column_name = 'adminpanel_genre.slug'
            else :
             column_name = 'adminpanel_genre.id'

            cursor.execute("select * from adminpanel_genre ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        else :
         column_name = 'adminpanel_genre.id'
         cursor.execute("select * from adminpanel_genre ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        all_genres = dictfetchall(cursor)
        docs_dict = {
            'total': totalrows,
            'rows': [{'id': all_genre['id'],
                      'title': all_genre['title'],
                      'createdate': formats.date_format(all_genre['created_date'], "Y-m-d"),
                      'details': all_genre['id'],
                     } for all_genre in all_genres]
        }
        return JsonResponse(docs_dict)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_genre(request):
    if 'admin_id' in request.session:
       
        if request.POST:
            import re
            title = request.POST.get('text','NONE')
            text = request.POST.get('text','NONE')
            create_slug = title.lower()
            create_slug = create_slug.replace (" ", "-")
            create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
            
            if Genre.objects.filter(slug=create_slug).exists():
                count_slugs = Genre.objects.filter(slug__contains=create_slug).count()
                create_slug = create_slug+"-"+str(count_slugs)
            
            genre = Genre(
                title=title,
                slug=create_slug,
                text = text,
            )
            genre.save()
            
            return HttpResponseRedirect('/admin/genre/')

        return render(request, 'adminpanel/add_genre.html',{})
    else :
       return HttpResponseRedirect('/admin/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def genre_details(request,id):
    if 'admin_id' in request.session:
            if id :
                if Genre.objects.filter(pk=id).exists():
                    genre=Genre.objects.get(pk=id)
                else :
                    return HttpResponseRedirect('/admin/genre/')
            else :
                return HttpResponseRedirect('/admin/genre/')

            return render(request, 'adminpanel/edit_genre.html',{'genre': genre })
    else :
       return HttpResponseRedirect('/admin/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_genre(request):
    if request.method == 'POST' and 'btn_edit' in request.POST :
       import re
       genre_id = request.POST.get('genre_id','NONE')
       title = request.POST.get('title','NONE')
       text = request.POST.get('text','NONE')

       create_slug = title.lower()
       create_slug = create_slug.replace (" ", "-")
       create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
       
       if Genre.objects.filter(slug=create_slug).exists():
            genre_slugcheck=Genre.objects.get(slug=create_slug)
            if genre_slugcheck.id!=int(genre_id):
               count_slugs = Genre.objects.filter(slug__contains=create_slug).count()
               create_slug = create_slug+"-"+str(count_slugs)
       
                
       genre_edit=Genre.objects.get(pk=int(genre_id))
       genre_edit.title=title
       genre_edit.slug=create_slug
       genre_edit.text = text
       genre_edit.save()
       
       
       return HttpResponseRedirect('/admin/genre-details/'+genre_id+'/')
    
    elif request.method == 'POST' and 'btn_delete' in request.POST :
        genre_id = request.POST.get('genre_id','NONE')
        res = delete_genre(genre_id)
        if res == 1 :
            return HttpResponseRedirect('/admin/login/') 
        else :
            return HttpResponseRedirect('/admin/genre/') 
    else :
       return HttpResponseRedirect('/admin/login/')    

def delete_genre(delete_id):
    if Genre.objects.filter(pk=int(delete_id)).exists():
        Genre.objects.filter(pk=int(delete_id)).delete()
        c = Genre.objects.filter(pk=int(delete_id)).count()
        if c:
           return 1   
        else:
            return 0
    else:
           return 1  
       
