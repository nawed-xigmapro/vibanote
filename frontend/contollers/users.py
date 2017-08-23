from django.shortcuts import render
from django.template import context, Template,Context,RequestContext
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from adminpanel.models import *
from django.contrib import messages
from django.db import connection
import PIL
from PIL import Image
from django.core.validators import validate_email
from datetime import datetime
import os
from os.path import basename
from django.conf import settings
from django.core.mail import send_mail
from frontend.contollers.commonctrl import *
from django.views.decorators.cache import cache_control


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user(request):
        import json
        email = password = ''
        rtn_obj = {}
        if request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                userprofile = UserProfile.objects.get(user_id=user.id)
                if user.check_password(password):
                    if user.is_active:
                        login(request, user)
                        request.session['member_id'] = user.id
                        userprofile.is_loggedin = 1
                        userprofile.save()
                        rtn_obj['ack'] = "1"
                        rtn_obj['msg'] = "LoggedIn! Please Wait for a momment redirecting.."
                        data = json.dumps(rtn_obj)
                        return HttpResponse(data)
                    else:
                       rtn_obj['ack'] = "0"
                       rtn_obj['msg'] = "Your account is under admin verification.Kindly contact Vibanote admin for further details."
                       data = json.dumps(rtn_obj)
                       return HttpResponse(data) 
                else :
                    rtn_obj['ack'] = "0"
                    rtn_obj['msg'] = "Your Password is incorrect."
                    data = json.dumps(rtn_obj)
                    return HttpResponse(data)  
            else:
                rtn_obj['ack'] = "0"
                rtn_obj['msg'] = "Your email is incorrect."
                data = json.dumps(rtn_obj)
                return HttpResponse(data)   
              
            
            
@cache_control(no_cache=True, must_revalidate=True, no_store=True)            
def register_user(request):
    import json
    import base64
    import time
    
    name=request.POST['name']
    rstr = int(time.time())
    new_str = name.replace(" ","-")
    username=new_str+str(rstr)
    password=request.POST['password']
    email=request.POST['email']
    if request.POST['phone']:
        phone=request.POST['phone']
    else:
        phone=None
    genre_id=request.POST['genre_id']
    phone_code=request.POST['phone_code']
    country=request.POST['country']
    rtn_obj = {}
    
    if request.method == 'POST':
        if User.objects.filter(username=username).exists(): 
            rtn_obj['ack'] = "0"
            rtn_obj['msg'] = "username Exists!"
            data = json.dumps(rtn_obj)
            return HttpResponse(data)
        elif User.objects.filter(email=email).exists(): 
             rtn_obj['ack'] = "0"
             rtn_obj['msg'] = "This email is already registered with us!"
             data = json.dumps(rtn_obj)
             return HttpResponse(data)
        else :
            try:
                validate_email(email)
            except validate_email.ValidationError:
                rtn_obj['ack'] = "0"
                rtn_obj['msg'] = "Invalid Email!"
                data = json.dumps(rtn_obj)
                return HttpResponse(data)
                
            user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    is_active=True
                )
            user.save()
            #Save userinfo record
            new_profile = UserProfile(
                    user=user,
                    name=name,
                    phone=phone,
                    phone_code=phone_code,
                    country=country,
                    genre_id=genre_id
                )
            new_profile.save() 
            request.session['member_id'] = user.id
            admininfo = User.objects.get(pk=1)
            mailpwd = password
            mailfname = request.POST['name']
                
            register_mail=EmailTemplates.objects.get(pk=2) 
                
            t = Template(register_mail.templatebody)
            c = Context({'email': email, 'password': mailpwd , 'name': mailfname})
            msg_html = t.render(c)
            send_mail("Vibanote Registration Mail", 'hello world again', admininfo.email, [email], html_message=msg_html)
                
                
                
            register_mail=EmailTemplates.objects.get(pk=3) 
            t = Template(register_mail.templatebody)
            c = Context({'email': email, 'password': mailpwd , 'name': mailfname})
            msg_html = t.render(c)
            send_mail("Vibanote Registration Mail", 'hello world again', email, [admininfo.email], html_message=msg_html)
            messages.add_message(request, messages.SUCCESS, 'Welcome To Vibanote.You have registered succesfully.Kindly check your email.')     
            rtn_obj['ack'] = "1"
            rtn_obj['msg'] = "Welcome To Vibanote.You have registered succesfully.Kindly check your email."
            data = json.dumps(rtn_obj)
            return HttpResponse(data)     
            
@cache_control(no_cache=True, must_revalidate=True, no_store=True)            
def logout_page(request):
    userprofile = UserProfile.objects.get(user_id=request.session['member_id'])
    userprofile.is_loggedin = 0
    userprofile.save()
    logout(request)
    return HttpResponseRedirect('/')   

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgot_password(request):
    if 'member_id' not in request.session:
        if request.method == 'POST':
            import json
            rtn_obj = {}
            if User.objects.filter(email=request.POST['email']).exists() :
              forgotuser = User.objects.get(email=request.POST['email'])  
              userprofile = UserProfile.objects.get(user_id=forgotuser.id)
              import time
              forgot_string = int(time.time()) 
              userprofile.forgotstr = forgot_string
              userprofile.save()
              name = userprofile.name
              admininfo = ns_get_user(1)
              forgot_link = "http://"+request.get_host()+"/forgotlink/"+str(forgot_string)
              forgot_mail=EmailTemplates.objects.get(pk=4) 
              t = Template(forgot_mail.templatebody)
              c = Context({'name': name, 'forgot_link' : forgot_link })
              msg_html = t.render(c)
              send_mail(forgot_mail.subject, 'hello world again', admininfo.email, [forgotuser.email], html_message=msg_html)
              
              rtn_obj['ack'] = "1"
              rtn_obj['link'] = forgot_string
              rtn_obj['msg'] = "Link Send to mail!"
              data = json.dumps(rtn_obj)
              return HttpResponse(data)
            else :
                rtn_obj['ack'] = "0"
                rtn_obj['msg'] = "Email Not exists!"
                data = json.dumps(rtn_obj)
                return HttpResponse(data)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgot_link(request,forgot_id): 
    if 'member_id' not in request.session:
        if UserProfile.objects.filter(forgotstr=forgot_id).exists() : 
            userprofile=UserProfile.objects.get(forgotstr=forgot_id)
            return render(request,'frontend/reset-password.html',{ 'userprofile': userprofile })
        else :
           return HttpResponseRedirect('/')   
    else :
       return HttpResponseRedirect('/')   
   
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset_password(request):
    if 'member_id' not in request.session:
        if request.POST :
            user_id = request.POST['user_id']
            forgot_id = request.POST['forgot_id']
            newpassword=request.POST['newpassword']
            confirmpassword=request.POST['confirmpassword'] 
            if newpassword != confirmpassword :
              return HttpResponseRedirect('/forgotlink/'+forgot_id+'/')
            userprofile=UserProfile.objects.get(user_id=user_id)
            user=User.objects.get(pk=user_id)
            user.set_password(newpassword) 
            user.save()
            userprofile.forgotstr = ""
            userprofile.save()
            messages.add_message(request, messages.SUCCESS, 'Password Changed!')   
            return HttpResponseRedirect('/')
        else :
           return HttpResponseRedirect('/') 
    else :
        return HttpResponseRedirect('/')   
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):    
    if 'member_id' in request.session:
        user_id = request.session['member_id']
        return render(request,'frontend/dashboard.html',{ 'user_id': user_id }) 
    else :
        return HttpResponseRedirect('/')  
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):    
    if 'member_id' in request.session:
        user_id = request.session['member_id']
        return render(request,'frontend/profile.html',{ 'user_id': user_id }) 
    else :
        return HttpResponseRedirect('/') 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile_edit(request):   
    if 'member_id' in request.session:
        user_id = request.session['member_id']
        #user = User.objects.get(pk=user_id)
        #userprofile = UserProfile.objects.get(user_id=user_id)
        if request.method == 'POST' and 'btn_edit' in request.POST :
                #edit_id=request.POST['edituser_id']
                uprofile_update = UserProfile.objects.get(user_id=int(user_id))
                #user_edit = User.objects.get(pk=int(user_id))
                #user_edit.first_name=request.POST.get('fname', "NONE")
                #user_edit.last_name=request.POST.get('lname', "NONE")
                #user_edit.save()
                
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
                return HttpResponseRedirect('/profile/')
        else :
            messages.add_message(request, messages.ERROR, 'Method not supported!')  
            return HttpResponseRedirect('/profile/')
        
    else : 
        return HttpResponseRedirect('/')    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pic_upload(request):
    if 'member_id' in request.session:
        user_id = request.session['member_id']
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
def artist_details(request,username):
    #user = User.objects.get(username=username)  
    cursor = connection.cursor()
    cursor.execute("select usr.*,up.*,ac.name as country_name from adminpanel_userprofile as up INNER JOIN auth_user as usr ON up.user_id = usr.id" 
    " INNER JOIN adminpanel_countries as ac ON up.country=ac.id where usr.username="+"'"+str(username)+"'" )
    user=query_to_dicts(cursor)
    user_genre = user['genre_id']
    user_id = user['user_id']
    cursor.execute("select usr.*,up.*,ac.name as country_name from adminpanel_userprofile as up INNER JOIN auth_user as usr ON up.user_id = usr.id" 
    " INNER JOIN adminpanel_countries as ac ON up.country=ac.id where up.genre_id="+"'"+str(user_genre)+"' and usr.id<>"+str(user_id)+" order by usr.id desc limit 6" )
    related_artists = dictfetchall(cursor)
    albums = Album.objects.filter(uploadby_id=user_id,is_approved=1)
    tracks = Tracks.objects.filter(uploadby_id=user_id,is_approved=1)
    videos = Video.objects.filter(uploadby_id=user_id,is_approved=1)
    return render(request,'frontend/artist-details.html',{ 'albums': albums, 'tracks': tracks, 'videos':videos, 'user' : user, 'related_artists' : related_artists  }) 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def change_password(request):
    if 'member_id' in request.session:
        if request.method == 'POST':
            user = User.objects.get(pk=request.session['member_id'])
            newpassword=request.POST['newpassword']
            confirmpassword=request.POST['confirmpassword']
            oldpassword = request.POST['oldpassword']
            if newpassword != confirmpassword :
              messages.add_message(request, messages.ERROR, 'new and conform password didnot match!')   
              return HttpResponseRedirect('/change-password/')
            user_authen = authenticate(username=user.username, password=oldpassword)
            if user_authen is not None:
                    user.set_password(newpassword) 
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'Password Changed!')  
                    return HttpResponseRedirect('/change-password/')
            else :
                messages.add_message(request, messages.ERROR, 'incorrect old password!')   
                return HttpResponseRedirect('/change-password/')
        return render(request,'frontend/change-password.html',{})
    else :
       return HttpResponseRedirect('/')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_mostbrowsed(request):
    if request.method == 'POST':
        user_id=request.POST.get('user_id', None)
        uprofile_update = UserProfile.objects.get(user_id=int(user_id))
        most_browsed = int(uprofile_update.most_browsed)+int(1)
        uprofile_update.most_browsed=most_browsed
        uprofile_update.save()
        return HttpResponse("1")
    else : 
        return HttpResponse("0")    
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_send_message(request):    
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
    
def show_messages(request):
    if 'member_id' in request.session:
        user_id = request.session['member_id']
        cursor = connection.cursor()
        #cursor.execute("SELECT * FROM adminpanel_messages WHERE id IN (SELECT MAX(id) FROM adminpanel_messages where touser_id ="+str(user_id)+" GROUP BY thread_id) order by msg_date desc")
        cursor.execute("SELECT * FROM adminpanel_messages WHERE touser_id ="+str(user_id)+" and FIND_IN_SET('"+str(user_id)+"',is_deleted_thread) < 1 GROUP BY thread_id order by msg_date desc")
        threads = dictfetchall(cursor)
        return render(request,'frontend/messages.html',{'threads':threads})
    else :
       return HttpResponseRedirect('/') 
   
def show_sent_messages(request):
    if 'member_id' in request.session:
        user_id = request.session['member_id']
        cursor = connection.cursor()
        #cursor.execute("SELECT * FROM adminpanel_messages WHERE id IN (SELECT MAX(id) FROM adminpanel_messages where fromuser_id ="+str(user_id)+" GROUP BY thread_id) order by msg_date desc")
        cursor.execute("SELECT * FROM adminpanel_messages where fromuser_id ="+str(user_id)+" and FIND_IN_SET('"+str(user_id)+"',is_deleted_thread) < 1 GROUP BY thread_id order by msg_date desc")
        threads = dictfetchall(cursor)
        return render(request,'frontend/sent-messages.html',{'threads':threads})
    else :
       return HttpResponseRedirect('/')    
   
def get_user_messages(request):
    if 'member_id' in request.session:
        thread_id=request.POST['thread_id']
        thread_type=request.POST['thread_type']
        user_id = request.session['member_id']
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
        
        msg_html = render_to_string('frontend/ajax_messages.html', {'messages': messages, 'user_id':user_id, 'thread_id':thread_id, 'reply_userid':reply_userid,'thread_type':thread_type },request=request)
        return HttpResponse(msg_html)
    else :
       return HttpResponseRedirect('/')     
   


def user_delete_thread(request):
    if 'member_id' in request.session:
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
    
def user_delete_msg(request):
    res_json = {}
    import json
    if 'member_id' in request.session:
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
    
    
def user_read_thread(request):
    if 'member_id' in request.session:
        user_id = request.session['member_id']
        msg_count = Messages.objects.filter(touser_id=user_id).update(is_read_to=1)
        if msg_count > 0 :
            return HttpResponse("1")
        else:
            return HttpResponse("0")
    else :
       return HttpResponse("0")   