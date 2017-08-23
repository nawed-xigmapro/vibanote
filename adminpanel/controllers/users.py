from django.template import context,Template,Context
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db import connection
from django.utils import formats
from adminpanel.models import *
from django.contrib import messages
from django.core.mail import send_mail,EmailMessage
from django.views.decorators.cache import cache_control
from django.template.loader import render_to_string
from django.utils.html import format_html
# Create your views here.
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
                        messages.add_message(request, messages.SUCCESS, 'Logged In!')
                        return HttpResponseRedirect('/admin/artists/')
                    else:
                      msg_error = "Your account is not active, please contact the site admin."
                      messages.add_message(request, messages.ERROR, msg_error)
                      return HttpResponseRedirect('/admin/login/')
                else:
                    msg_error = "you are not admin!"
                    messages.add_message(request, messages.ERROR, msg_error)
                    return HttpResponseRedirect('/admin/login/')
            else:
                msg_error = "Your username and/or password were incorrect."
                messages.add_message(request, messages.ERROR, msg_error)
                return HttpResponseRedirect('/admin/login/')
    
        return render(request, 'adminpanel/login.html', {})            
 
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/admin/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
         cursor.execute("select adminpanel_userprofile.name, adminpanel_userprofile.picture, auth_user.id ,auth_user.email,auth_user.username,auth_user.first_name,auth_user.last_name,auth_user.is_active from auth_user INNER JOIN adminpanel_userprofile"
         " ON auth_user.id = adminpanel_userprofile.user_id where auth_user.username like '"+srch+"%' and auth_user.id!=1 ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' in request.GET :
            srch = request.GET['search']
            sort = request.GET['sort']
            if sort == "username":
                column_name = 'auth_user.username'
            elif sort == "email":
                column_name = 'auth_user.email'
            elif sort == "isactive":
                column_name = 'auth_user.is_active'    
            else :
             column_name = 'adminpanel_userprofile.name'

            if srch :
              cursor.execute("select adminpanel_userprofile.name, adminpanel_userprofile.picture, auth_user.id ,auth_user.email,auth_user.username,auth_user.first_name,auth_user.last_name,auth_user.is_active from auth_user INNER JOIN adminpanel_userprofile"
              " ON auth_user.id = adminpanel_userprofile.user_id where auth_user.username like '"+srch+"%' and auth_user.id!=1 ORDER BY "+column_name+" "+order+" LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])
            else:
             cursor.execute("select adminpanel_userprofile.name, adminpanel_userprofile.picture, auth_user.id ,auth_user.email,auth_user.username,auth_user.first_name,auth_user.last_name,auth_user.is_active from auth_user INNER JOIN adminpanel_userprofile"
             " ON auth_user.id = adminpanel_userprofile.user_id where auth_user.id!=1 ORDER BY "+column_name+" "+order+" LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' not in request.GET:
            sort = request.GET['sort']
            if sort == "username":
                column_name = 'auth_user.username'
            elif sort == "email":
                column_name = 'auth_user.email'
            elif sort == "isactive":
                column_name = 'auth_user.is_active'    
            else :
             column_name = 'adminpanel_userprofile.name'

            cursor.execute("select adminpanel_userprofile.name, adminpanel_userprofile.picture, auth_user.id ,auth_user.email,auth_user.username,auth_user.first_name,auth_user.last_name,auth_user.is_active from auth_user INNER JOIN adminpanel_userprofile"
            " ON auth_user.id = adminpanel_userprofile.user_id where auth_user.id!=1 ORDER BY "+column_name+" "+order+" LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        else :
         order = "DESC"   
         column_name = 'auth_user.id'
         cursor.execute("select adminpanel_userprofile.name, adminpanel_userprofile.picture, auth_user.id ,auth_user.email,auth_user.username,auth_user.first_name,auth_user.last_name,auth_user.is_active from auth_user INNER JOIN adminpanel_userprofile"
         " ON auth_user.id = adminpanel_userprofile.user_id where auth_user.id!=1 ORDER BY "+column_name+" "+order+" LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        all_users = dictfetchall(cursor)
        docs_dict = {
            'total': totalrows,
            'rows': [{
                      'name': all_user['name'],
                      'email': all_user['email'],
                      'isactive': all_user['is_active'],
                      'id': all_user['id'],
                      'uid': all_user['id'],
                      'thumbnail': all_user['picture'],
                      'videos': all_user['id'],
                      'tracks': all_user['id'],
                      'albums': all_user['id'],
                      'contact': all_user['id'],
                      } for all_user in all_users]
        }
        return JsonResponse(docs_dict) 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_userdetails(request,user_id):
    if 'admin_id' in request.session:
        if User.objects.filter(pk=int(user_id)).exists():
            userdetails = UserProfile.objects.get(user_id=user_id)
            current_user = User.objects.get(pk=user_id)
            return render(request,'adminpanel/userdetails.html', {'userinfo': userdetails, 'current_user' : current_user , 'user_id' : user_id })
        else:
           messages.add_message(request, messages.ERROR, 'user not exists!')    
           return HttpResponseRedirect('/admin/artists/')    
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
            return HttpResponse(3) # 3 means data is not in post
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
            return HttpResponse(3) # 3 means data is not in post
    else :
          return HttpResponse(2) # 2 means admin is not logged in 
      
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgotpasswordform(request):
    if 'admin_id' not in request.session:
        return render(request,'adminpanel/forgotpassword.html',{})
    else:
       return HttpResponseRedirect('/admin/artists/')   

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgot_password(request):
    if 'admin_id' not in request.session:
        if request.method == 'POST':
            if User.objects.filter(email=request.POST['email']).exists() :
              forgotuser = User.objects.get(email=request.POST['email'])  
              userprofile = UserProfile.objects.get(user_id=forgotuser.id)
              import time
              forgot_string = int(time.time()) 
              userprofile.forgotstr = forgot_string
              userprofile.save()
              name = userprofile.name
              forgot_link = "http://"+request.get_host()+"/admin/forgotlink/"+str(forgot_string)
              forgot_mail=EmailTemplates.objects.get(pk=4) 
              t = Template(forgot_mail.templatebody)
              c = Context({'name': name, 'forgot_link' : forgot_link })
              msg_html = t.render(c)
              send_mail(forgot_mail.subject, 'hello world again', 'nawed@xigmapro.com', [forgotuser.email], html_message=msg_html)
              
              messages.add_message(request, messages.SUCCESS, 'link Send to mail!')   
              return HttpResponseRedirect('/admin/forgot-password/')
            else :
                messages.add_message(request, messages.ERROR, 'Email not exists!')   
                return HttpResponseRedirect('/admin/forgot-password/')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgot_link(request,forgot_id): 
    if 'admin_id' not in request.session:
        if UserProfile.objects.filter(forgotstr=forgot_id).exists() : 
            userprofile=UserProfile.objects.get(forgotstr=forgot_id)
            return render(request,'adminpanel/reset-password.html',{ 'userprofile': userprofile })
        else :
           return HttpResponseRedirect('/admin/login/')   
    else :
       return HttpResponseRedirect('/admin/artists/')   
   
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset_password(request):
    if 'admin_id' not in request.session:
        if request.POST :
            user_id = request.POST['user_id']
            forgot_id = request.POST['forgot_id']
            newpassword=request.POST['newpassword']
            confirmpassword=request.POST['confirmpassword'] 
            if newpassword != confirmpassword :
              return HttpResponseRedirect('/admin/forgotlink/'+forgot_id+'/')
            userprofile=UserProfile.objects.get(user_id=user_id)
            user=User.objects.get(pk=user_id)
            user.set_password(newpassword) 
            user.save()
            userprofile.forgotstr = ""
            userprofile.save()
            messages.add_message(request, messages.SUCCESS, 'Password Changed!')   
            return HttpResponseRedirect('/admin/login/')
        else :
           return HttpResponseRedirect('/admin/login/') 
    else :
        return HttpResponseRedirect('/admin/artists/')    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_change_password(request):
    if 'admin_id' in request.session:
        if request.method == 'POST':
            user = User.objects.get(pk=request.session['admin_id'])
            newpassword=request.POST['newpassword']
            confirmpassword=request.POST['confirmpassword']
            oldpassword = request.POST['oldpassword']
            if newpassword != confirmpassword :
              messages.add_message(request, messages.ERROR, 'new and conform password didnot match!')   
              return HttpResponseRedirect('/admin/password-change/')
            user_authen = authenticate(username=user.username, password=oldpassword)
            if user_authen is not None:
                    user.set_password(newpassword) 
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'Password Changed!')  
                    return HttpResponseRedirect('/admin/logout/')
            else :
                messages.add_message(request, messages.ERROR, 'incorrect old password!')   
                return HttpResponseRedirect('/admin/password-change/')
        return render(request,'adminpanel/change-password.html',{})        
    else :
       return HttpResponseRedirect('/admin/login/')  
   
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_change_email(request):
    if 'admin_id' in request.session:
        if request.method == 'POST':
            user = User.objects.get(pk=request.session['admin_id'])
            newemail=request.POST['newemail']
            oldemail = request.POST['oldemail']
            if oldemail != user.email :
              messages.add_message(request, messages.ERROR, 'Current email entered was wrong!')   
              return HttpResponseRedirect('/admin/email-change/')
            elif oldemail == newemail :
                messages.add_message(request, messages.ERROR, 'Current email and new email cannot be same!')   
                return HttpResponseRedirect('/admin/email-change/')
            elif User.objects.filter(email=newemail).exclude(pk=request.session['admin_id']).exists():
                 messages.add_message(request, messages.ERROR, 'Already a user cannot be admin!')   
                 return HttpResponseRedirect('/admin/email-change/')
            else:
                user.email = newemail
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Email Changed!')  
                return HttpResponseRedirect('/admin/email-change/')
            
        return render(request,'adminpanel/change-email.html',{})        
    else :
       return HttpResponseRedirect('/admin/login/')     
   
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_user_edit(request):   
    if 'admin_id' in request.session:
        user_id = request.POST['edit_id']
        if request.method == 'POST' and 'btn_edit' in request.POST :
                email = request.POST.get('email', None)
                if User.objects.filter(email=email).exclude(pk=user_id).exists(): 
                    messages.add_message(request, messages.ERROR, 'user with same email already exists!')  
                    return HttpResponseRedirect('/admin/userdetails/'+user_id+"/")
                    
                uprofile_update = UserProfile.objects.get(user_id=int(user_id))
                user_edit = User.objects.get(pk=int(user_id))
                user_edit.email=email
                #user_edit.last_name=request.POST.get('lname', "NONE")
                user_edit.save()
                
                uprofile_update.dob=datetime.strptime(request.POST.get('dob', None), '%m-%d-%Y')
                uprofile_update.gender=request.POST.get('gender', None)
                uprofile_update.phone=request.POST.get('phone', None) 
                uprofile_update.address=request.POST.get('address', None)
                uprofile_update.name=request.POST.get('name', None)
                uprofile_update.city=request.POST.get('city', None)
                uprofile_update.state=request.POST.get('state', None)
                uprofile_update.phone_code=request.POST.get('phone_code', None)
                uprofile_update.description=request.POST.get('description', None)
                uprofile_update.country=request.POST.get('country', None)
                uprofile_update.website=request.POST.get('website', None)
                uprofile_update.save()
                messages.add_message(request, messages.SUCCESS, 'Profile Updated!')
                return HttpResponseRedirect('/admin/userdetails/'+user_id+"/")
        else :
            messages.add_message(request, messages.ERROR, 'Method not supported!')  
            return HttpResponseRedirect('/admin/userdetails/'+user_id+"/")
        
    else : 
        return HttpResponseRedirect('/admin/login/')    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_userpic_upload(request):
    if 'admin_id' in request.session:
        user_id = request.POST['edit_id']
        if len(request.FILES) != 0:
            uprofile_update = UserProfile.objects.get(user_id=int(user_id))
            if uprofile_update.picture :
                image_path = settings.MEDIA_ROOT+"/"+uprofile_update.picture.name
                os.unlink(image_path)
                uprofile_update.picture = request.FILES['picture']

            else :
                uprofile_update.picture = request.FILES['picture'] 

            uprofile_update.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Pic Updated!')  
            return HttpResponse("1")
        else :
            return HttpResponse("0")    
    else : 
        return HttpResponse("0")  
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_delete_users(request):
    if 'admin_id' in request.session:
        if request.method == 'POST': 
                user_id = request.POST['user_id']
                if User.objects.filter(pk=int(user_id)).exists():
                   User.objects.filter(pk=int(user_id)).delete()
                   c = User.objects.filter(pk=int(user_id)).count()
                   if c:
                      messages.add_message(request, messages.ERROR, 'artist cannot be deleted!') 
                      return HttpResponse("0")  
                   else:
                       messages.add_message(request, messages.SUCCESS, 'artist deleted successfully!')
                       return HttpResponse("1")
                else:
                    messages.add_message(request, messages.ERROR, 'artist didnot exists!')  
                    return HttpResponse("0")
        else:
            messages.add_message(request, messages.ERROR, 'Method not supported!')  
            return HttpResponse("0")   
    else:
        messages.add_message(request, messages.ERROR, 'Not an admin!')  
        return HttpResponse("0")    
    
def admin_inbox_messages(request):
    if 'admin_id' in request.session:
        user_id = request.session['admin_id']
        cursor = connection.cursor()
        #cursor.execute("SELECT * FROM adminpanel_messages WHERE id IN (SELECT MAX(id) FROM adminpanel_messages where touser_id ="+str(user_id)+" GROUP BY thread_id) order by msg_date desc")
        cursor.execute("SELECT * FROM adminpanel_messages WHERE touser_id ="+str(user_id)+" and FIND_IN_SET('"+str(user_id)+"',is_deleted_thread) < 1 GROUP BY thread_id order by msg_date desc")
        threads = dictfetchall(cursor)
        return render(request,'adminpanel/inbox-msg.html',{'threads':threads})
    else :
       return HttpResponseRedirect('/') 
   
def admin_outbox_messages(request):
    if 'admin_id' in request.session:
        user_id = request.session['admin_id']
        cursor = connection.cursor()
        #cursor.execute("SELECT * FROM adminpanel_messages WHERE id IN (SELECT MAX(id) FROM adminpanel_messages where fromuser_id ="+str(user_id)+" GROUP BY thread_id) order by msg_date desc")
        cursor.execute("SELECT * FROM adminpanel_messages where fromuser_id ="+str(user_id)+" and FIND_IN_SET('"+str(user_id)+"',is_deleted_thread) < 1 GROUP BY thread_id order by msg_date desc")
        threads = dictfetchall(cursor)
        return render(request,'adminpanel/sent-msg.html',{'threads':threads})
    else :
       return HttpResponseRedirect('/')      
   
   
def get_thread_detail(request):
    if 'admin_id' in request.session:
        thread_id=request.POST['thread_id']
        thread_type=request.POST['thread_type']
        user_id = request.session['admin_id']
        reply_userid = ""
        Messages.objects.filter(thread_id=thread_id,touser_id=user_id).update(is_new_thread=0)
        messages = Messages.objects.filter(thread_id=thread_id).exclude(is_deleted_msg__contains=str(user_id)).order_by('-msg_date')
        for message in messages:
            if message.fromuser_id !=user_id:
               reply_userid = message.fromuser_id
               break
        if reply_userid == "":
            messages_reply = Messages.objects.filter(thread_id=thread_id).order_by('-msg_date')
            for msg in messages_reply:
                if msg.fromuser_id !=user_id:
                    reply_userid = msg.fromuser_id
                    break       
        msg_html = render_to_string('adminpanel/ajax_admin_messages.html', {'messages': messages, 'user_id':user_id, 'thread_id':thread_id, 'reply_userid':reply_userid,'thread_type':thread_type },request=request)
        return HttpResponse(msg_html)
    else :
       return HttpResponseRedirect('/')    
   
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_user_send_message(request):    
    if request.method == 'POST':  
        touser_id=request.POST['touser_id']
        fromuser_id=request.POST['fromuser_id']
        subject=request.POST['subject']
        body=request.POST['body']
        thread_id=request.POST['thread_id']
        if thread_id == "0":
            import time
            rstr = int(time.time())
            thread_id = str("msg-")+str(rstr)
            
        add_message = Messages(
            touser_id=touser_id,
            fromuser_id=fromuser_id,
            subject=subject,
            body=body,
            is_new_thread=1,
            thread_id=thread_id
        )
        add_message.save()
        Messages.objects.filter(thread_id=thread_id,touser_id=touser_id).update(is_new_thread=1)
        return HttpResponse("1")            
    else : 
        return HttpResponse("0")     
    
def mass_mail_artists(request):
    if 'admin_id' in request.session:
        res_json = {}
        recepient_list = []
        import json
        if request.method == 'POST': 
            subject=request.POST['subject']
            text=request.POST['text']
            text_html = format_html(text)
            
            #text_render = Template(text)   # another way to format html
            #c = Context({'message': 'Your message'})
            #text_html = text_render.render(c)
            
            mass_user_mail=EmailTemplates.objects.get(pk=7) 
            t = Template(mass_user_mail.templatebody)
            c = Context({'approval_text' : subject,'edit_link' : text_html })
            msg_html = t.render(c)
            mail_recepeints=User.objects.all()
            admin_info = User.objects.get(pk=request.session['admin_id'])
            #tuples = tuple((subject,"", admin_info.email, [newsletter.email]) for newsletter in newsletters)
            #send_mass_mail(tuples,fail_silently=False)
            for mail_recepeint in mail_recepeints:
                recepient_list.append(mail_recepeint.email)
            
            #send_mail(subject,'Here is the message.',admin_info.email,recepient_list,fail_silently=False,html_message=msg_html)
            
            msg = EmailMessage(subject, msg_html, admin_info.email, [admin_info.email],recepient_list)
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send(fail_silently=False)
    
            res_json['ack'] = "1"
            res_json['msg'] = "Mail Send"
            res_json['msg_type'] = "success"
            data = json.dumps(res_json)
            #messages.add_message(request, messages.ERROR, 'Subscribeuser not exists!')
            return HttpResponse(data) 
        
        else:
            res_json['ack'] = "0"
            res_json['msg'] = "Not the right method"
            res_json['msg_type'] = "error"
            data = json.dumps(res_json)
            #messages.add_message(request, messages.ERROR, 'Subscribeuser not exists!')
            return HttpResponse(data)    
    
    else:
        res_json['ack'] = "0"
        res_json['msg'] = "Not in session"
        res_json['msg_type'] = "error"
        data = json.dumps(res_json)
        #messages.add_message(request, messages.ERROR, 'Subscribeuser not exists!')
        return HttpResponse(data)   
    
    
def admin_delete_thread(request):
    if 'admin_id' in request.session:
        if request.method == 'POST': 
            thread_id=request.POST['thread_id']
            user_id=request.POST['user_id']
            messages_del = Messages.objects.filter(thread_id=thread_id)
            for message in messages_del:
                single_msg = Messages.objects.get(pk=message.id)
                upadte_val = single_msg.is_deleted_thread
                if upadte_val == "0":
                    single_msg.is_deleted_thread = user_id
                else :
                    updated_value = str(upadte_val)+","+str(user_id)
                    single_msg.is_deleted_thread = updated_value
                
                single_msg.save()
                
            messages.add_message(request, messages.SUCCESS, 'Thread deleted')
            return HttpResponse(1) 
           
        
        else:
            messages.add_message(request, messages.ERROR, 'Not the right method')
            return HttpResponse(0)    
    
    else:
        messages.add_message(request, messages.ERROR, 'Not in session!')
        return HttpResponse(0)  
    
def admin_delete_msg(request):
    res_json = {}
    import json
    if 'admin_id' in request.session:
        if request.method == 'POST': 
            msg_id=request.POST['msg_id']
            user_id=request.POST['user_id']
            thread_id=request.POST['thread_id']
            single_msg = Messages.objects.get(pk=msg_id)
            upadte_val = single_msg.is_deleted_msg
            if upadte_val == "0":
                single_msg.is_deleted_msg = user_id
            else :
                updated_value = str(upadte_val)+","+str(user_id)
                single_msg.is_deleted_msg = updated_value
                
            single_msg.save()
            if Messages.objects.filter(thread_id=thread_id).exclude(is_deleted_msg__contains=str(user_id)).exists():
                res_json['ack'] = "1"
                res_json['msg'] = "Message deleted"
                res_json['msg_type'] = "success"
                data = json.dumps(res_json)
                #messages.add_message(request, messages.ERROR, 'Subscribeuser not exists!')
                return HttpResponse(data)
            else :
                Messages.objects.filter(thread_id=thread_id,is_deleted_msg__contains=str(user_id)).update(is_deleted_thread=1)
                res_json['ack'] = "2"
                res_json['msg'] = "Message deleted"
                res_json['msg_type'] = "success"
                data = json.dumps(res_json)
                #messages.add_message(request, messages.ERROR, 'Subscribeuser not exists!')
                return HttpResponse(data)
           
        else:
            res_json['ack'] = "0"
            res_json['msg'] = "Not the right method"
            res_json['msg_type'] = "error"
            data = json.dumps(res_json)
            #messages.add_message(request, messages.ERROR, 'Subscribeuser not exists!')
            return HttpResponse(data)
    
    else:
        res_json['ack'] = "0"
        res_json['msg'] = "Not in session"
        res_json['msg_type'] = "error"
        data = json.dumps(res_json)
        #messages.add_message(request, messages.ERROR, 'Subscribeuser not exists!')
        return HttpResponse(data)
    
    
def admin_read_thread(request):
    if 'admin_id' in request.session:
        user_id = request.session['admin_id']
        msg_count = Messages.objects.filter(touser_id=user_id).update(is_read_to=1)
        if msg_count > 0 :
            return HttpResponse("1")
        else:
            return HttpResponse("0")
    else :
       return HttpResponse("0")
    
    
    
    
    
    
                
    