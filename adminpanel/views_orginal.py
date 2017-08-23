from django.template import context
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db import connection
from django.utils import formats
from .models import *

# Create your views here.
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def admin_login(request):
    if 'admin_id' in request.session:
        return HttpResponseRedirect('/admin/artists/')
    else:
        msg_error = ""
        username = password = ''
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            #print(request.POST.get('remember_me'))
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff :
                    if user.is_active:
                        login(request, user)
                        request.session['admin_id'] = user.id
                        return HttpResponseRedirect('/admin/artists/')
                    else:
                      msg_error = "Your account is not active, please contact the site admin."
                else:
                    msg_error = "you are not admin!"
            else:
                msg_error = "Your username and/or password were incorrect."

 
    return render(request, 'adminpanel/login.html',{'msg_error': msg_error}, context)


def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/admin/login/')

def artist_list(request):
    if 'admin_id' in request.session:
       return render(request, 'adminpanel/artist-list.html')
    else :
     return HttpResponseRedirect('/admin/login/') 
 
def get_artist_list(request):
        cursor = connection.cursor()
        cursor.execute("select count(*) as total from auth_user INNER JOIN adminpanel_userprofile"
        " ON auth_user.id = adminpanel_userprofile.user_id where auth_user.id!=1")
        
        row = cursor.fetchone()
        totalrows = row[0]
        
        order = request.GET['order']

        if 'search' in request.GET and 'sort' not in request.GET :
         column_name = 'auth_user.username'
         srch = request.GET['search']
         cursor.execute("select auth_user.id ,auth_user.email,auth_user.username,auth_user.first_name,auth_user.last_name from auth_user INNER JOIN adminpanel_userprofile"
         " ON auth_user.id = adminpanel_userprofile.user_id where auth_user.username like '"+srch+"%' and auth_user.id!=1 ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' in request.GET :
            srch = request.GET['search']
            sort = request.GET['sort']
            if sort == "username":
                column_name = 'auth_user.username'
            elif sort == "email":
                column_name = 'auth_user.email'
            else :
             column_name = 'auth_user.first_name'

            if srch :
              cursor.execute("select auth_user.id ,auth_user.email,auth_user.username,auth_user.first_name,auth_user.last_name from auth_user INNER JOIN adminpanel_userprofile"
              " ON auth_user.id = adminpanel_userprofile.user_id where auth_user.username like '"+srch+"%' and auth_user.id!=1 ORDER BY "+column_name+" "+order+" LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])
            else:
             cursor.execute("select auth_user.id ,auth_user.email,auth_user.username,auth_user.first_name,auth_user.last_name from auth_user INNER JOIN adminpanel_userprofile"
             " ON auth_user.id = adminpanel_userprofile.user_id where auth_user.id!=1 ORDER BY "+column_name+" "+order+" LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' not in request.GET:
            sort = request.GET['sort']
            if sort == "username":
                column_name = 'auth_user.username'
            elif sort == "email":
                column_name = 'auth_user.email'
            else :
             column_name = 'auth_user.first_name'

            cursor.execute("select auth_user.id ,auth_user.email,auth_user.username,auth_user.first_name,auth_user.last_name from auth_user INNER JOIN adminpanel_userprofile"
            " ON auth_user.id = adminpanel_userprofile.user_id where auth_user.id!=1 ORDER BY "+column_name+" "+order+" LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        else :
         column_name = 'auth_user.id'
         cursor.execute("select auth_user.id ,auth_user.email,auth_user.username,auth_user.first_name,auth_user.last_name from auth_user INNER JOIN adminpanel_userprofile"
         " ON auth_user.id = adminpanel_userprofile.user_id where auth_user.id!=1 ORDER BY "+column_name+" "+order+" LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        all_users = dictfetchall(cursor)
        docs_dict = {
            'total': totalrows,
            'rows': [{
                      'name': all_user['first_name']+" "+all_user['last_name'],
                      'username': all_user['username'],
                      'email': all_user['email'],
                      'editid': all_user['id'],
                      'id': all_user['id'],
                      'uid': all_user['id'],
                      } for all_user in all_users]
        }
        return JsonResponse(docs_dict) 
    
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

def create_cms(request):
   if 'admin_id' in request.session:
       cms_title =""
       cms_content=""
       if request.POST:
            import re
            cms_title = request.POST.get('cms_title','NONE')
            cms_content = request.POST.get('cms_content','NONE')

            create_slug = cms_title.lower()
            create_slug = create_slug.replace (" ", "-")
            create_slug = re.sub('[^a-zA-Z0-9 \n\.]', '-', create_slug)
            
            if Cms.objects.filter(slug=create_slug).exists():
                count_slugs = Cms.objects.filter(slug__contains=create_slug).count()
                create_slug = create_slug+"-"+str(count_slugs)
                
            create_cms = Cms(
                             title=cms_title,
                             slug=create_slug,
                             text = cms_content,
                             author_id = request.session['admin_id']
                             )
            create_cms.save()
            return HttpResponseRedirect('/admin/cms/')


       #return render_to_response('adminpanel/create_cms.html', {'cms_title': cms_title, 'cms_slug': cms_slug, 'cms_content': cms_content } , context_instance = RequestContext(request))
       return render(request, 'adminpanel/create_cms.html',{'cms_title': cms_title, 'cms_content': cms_content },context)
   else :
       return HttpResponseRedirect('/admin/login/')

def cms_details(request,cms_id):
   if 'admin_id' in request.session:
             if cms_id :
                         if Cms.objects.filter(pk=cms_id).exists():
                               cms_edit=Cms.objects.get(pk=cms_id)
                               cms_title = cms_edit.title
                               cms_content = cms_edit.text
                         else :
                           return HttpResponseRedirect('/admin/cms/')
             else :
                  return HttpResponseRedirect('/admin/cms/')


             #return render_to_response('adminpanel/edit_cms.html',{'cms_title': cms_title, 'cms_slug': cms_slug, 'cms_content': cms_content, 'cms_id' : cms_id } ,context_instance = RequestContext(request))
             return render(request, 'adminpanel/edit_cms.html',{'cms_title': cms_title, 'cms_content': cms_content, 'cms_id' : cms_id },context)
   else :
       return HttpResponseRedirect('/admin/login/')

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
       
def get_userdetails(request,user_id):
    if 'admin_id' in request.session:
            userdetails = UserProfile.objects.get(user_id=user_id)
            current_user = User.objects.get(pk=user_id)
            return render(request,'adminpanel/userdetails.html', {'userdetails': userdetails, 'current_user' : current_user , 'user_id' : user_id }, context)
    else :
       return HttpResponseRedirect('/admin/login/') 
   
def deactivate_users(request):
    if 'admin_id' in request.session:
        if request.method == 'POST':
            block_id = request.POST.get('block_id', "NONE")
            reason = request.POST.get('reason', "NONE")
            if User.objects.filter(pk=block_id).exists(): 
                    user_block=User.objects.get(pk=int(block_id))
                    user_block.is_active = False
                    user_block.save()
                    user_profileblock =UserProfile.objects.get(user_id=block_id)
                    user_profileblock.reason = reason
                    user_profileblock.save()
                    return HttpResponse(1) # 1 means user is blocked 
            else:
                return HttpResponse(0) # 0 means user not exists
        else :
            return HttpResponseRedirect(3) # 3 means data is not in post
    else :
          return HttpResponse(2) # 2 means admin is not logged in

def activate_users(request):
    if 'admin_id' in request.session:
        if request.method == 'POST':
            blocked_id = request.POST.get('blocked_id', "NONE")
            if User.objects.filter(pk=blocked_id).exists(): 
                    user_block=User.objects.get(pk=int(blocked_id))
                    user_block.is_active = True
                    user_block.save()
                    user_profileblock =UserProfile.objects.get(user_id=blocked_id)
                    user_profileblock.reason = ""
                    user_profileblock.save()
                    '''activate_mail=EmailTemplates.objects.get(pk=3) 
                    t = Template(activate_mail.templatebody)
                    c = Context({'name': user_block.first_name, 'msg_description': "Your Account is activated" })
                    msg_html = t.render(c)
                    send_mail("Account Activation", 'hello world again', 'nits.nawed@gmail.com', ['nits.nawed@gmail.com',user_block.email], html_message=msg_html)'''
                    return HttpResponse(1) # 1 means user is active now 
            else:
                return HttpResponse(0) # 0 means user not exists
        else :
            return HttpResponseRedirect(3) # 3 means data is not in post
    else :
          return HttpResponse(2) # 2 means admin is not logged in   
    
 