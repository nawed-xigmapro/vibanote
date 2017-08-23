from django.shortcuts import render
from django.template import context, Template
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

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def query_to_dicts(cursor):
    col_names = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    if row is None:
          row_dict = "" 
    else :      
        row_dict = dict(zip(col_names, row))
    return row_dict

# Create your views here.
def login_user(request):
        import json
        email = password = ''
        rtn_obj = {}
        if request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    request.session['member_id'] = user.id
                    rtn_obj['ack'] = "1"
                    rtn_obj['msg'] = "LoggedIn! Please Wait for a momment redirecting.."
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
              
            
            
            
def register_user(request):
    import json
    import base64
    import time
    #send_mail("test register mail", 'It is a test gmail smtp mail', 'soumen.deb@xigmapro.com', ['soumen.deb@xigmapro.com','avishekroy@xigmapro.com'])
    name=request.POST['name']
    rstr = int(time.time())
    username=name+str(rstr)
    password=request.POST['password']
    email=request.POST['email']
    phone=request.POST['phone']
    rtn_obj = {}
    
    if request.method == 'POST':
        if User.objects.filter(username=username).exists(): 
            rtn_obj['ack'] = "0"
            rtn_obj['msg'] = "username Exists!"
            data = json.dumps(rtn_obj)
            return HttpResponse(data)
        elif User.objects.filter(email=email).exists(): 
             rtn_obj['ack'] = "0"
             rtn_obj['msg'] = "Email Exists!"
             data = json.dumps(rtn_obj)
             return HttpResponse(data)
        else :
            try:
                validate_email(email)
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
                    phone=phone
                )
                new_profile.save()
                request.session['member_id'] = user.id
                send_mail("test register mail", 'It is a test gmail smtp mail', 'soumen.deb@xigmapro.com', ['soumen.deb@xigmapro.com','avishekroy@xigmapro.com'])
                print("hi");
                import pdb;pdb.set_trace()
                '''
                mailpwd = request.POST['password1']
                mailfname = request.POST['first_name']
                register_mail=EmailTemplates.objects.get(pk=2) 
                t = Template(register_mail.templatebody)
                c = Context({'username': user.username, 'password': mailpwd , 'firstname': mailfname, 'activation_link' : activation_link })
                msg_html = t.render(c)
                send_mail(register_mail.subject, 'hello world again', 'nits.nawed@gmail.com', ['nits.nawed@gmail.com',user.email], html_message=msg_html)
                '''
                rtn_obj['ack'] = "1"
                rtn_obj['msg'] = "Registerd! Please Wait for a momment redirecting.."
                data = json.dumps(rtn_obj)
                return HttpResponse(data)     
            except:
                rtn_obj['ack'] = "0"
                rtn_obj['msg'] = "Invalid Email!"
                data = json.dumps(rtn_obj)
                return HttpResponse(data)
            
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')   

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
              forgot_link = "http://http://127.0.0.1:8000/forgotstring/"+str(forgot_string)
              '''
              forgot_mail=EmailTemplates.objects.get(pk=6) 
              t = Template(forgot_mail.templatebody)
              c = Context({'name': name, 'forgot_link' : forgot_link })
              msg_html = t.render(c)
              send_mail(forgot_mail.subject, 'hello world again', 'nits.nawed@gmail.com', ['nits.nawed@gmail.com',forgotuser.email], html_message=msg_html)
              '''
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
    

def forgot_link(request,forgot_id): 
    if 'member_id' not in request.session:
        if UserProfile.objects.filter(forgotstr=forgot_id).exists() : 
            userprofile=UserProfile.objects.get(forgotstr=forgot_id)
            return render(request,'frontend/reset-password.html',{ 'userprofile': userprofile },context)
        else :
           return HttpResponseRedirect('/')   
    else :
       return HttpResponseRedirect('/')   
   
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
    

def dashboard(request):    
    if 'member_id' in request.session:
        user_id = request.session['member_id']
        return render(request,'frontend/dashboard.html',{ 'user_id': user_id },context) 
    else :
        return HttpResponseRedirect('/')  
    
def profile(request):    
    if 'member_id' in request.session:
        user_id = request.session['member_id']
        return render(request,'frontend/profile.html',{ 'user_id': user_id },context) 
    else :
        return HttpResponseRedirect('/') 
    
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
                
                uprofile_update.dob=datetime.strptime(request.POST.get('dob'), '%m-%d-%Y')
                uprofile_update.gender=request.POST.get('gender', "NONE")
                uprofile_update.phone=request.POST.get('phone', "NONE") 
                uprofile_update.address=request.POST.get('address', "NONE")
                uprofile_update.name=request.POST.get('name', "NONE")
                uprofile_update.city=request.POST.get('city', "NONE")
                uprofile_update.state=request.POST.get('state', "NONE")
                uprofile_update.description=request.POST.get('description', "NONE")
                uprofile_update.country=request.POST.get('country', "NONE")
                uprofile_update.website=request.POST.get('website', "NONE")
                uprofile_update.save()
                messages.add_message(request, messages.SUCCESS, 'Profile Updated!')
                return HttpResponseRedirect('/profile/')
        else :
            messages.add_message(request, messages.ERROR, 'Method not supported!')  
            return HttpResponseRedirect('/profile/')
        
    else : 
        return HttpResponseRedirect('/')    
    
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
    
        
                   