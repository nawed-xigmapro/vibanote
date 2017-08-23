from adminpanel.models import *
from django.shortcuts import render
from django.template import context,Template,Context
from django.core.mail import send_mail
# common functions throught the controller.

def get_genre():
    genre=Genre.objects.all()
    return genre

def get_type():
    types=Type.objects.all()
    return types
        
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
    
    
def get_states(request):    
    if request.method == 'POST':
        import json
        rtn_obj = {}
        results = []
        country_id = request.POST.get('country_id', None)
        if States.objects.filter(country_id=int(country_id)).exists():
            states=States.objects.filter(country_id=int(country_id)) 
            for state in states:
                res_json = {}
                res_json['value'] = state.id
                res_json['text'] = state.name
                results.append(res_json)
            json_states = json.dumps(results)
            rtn_obj['ack'] = "1"
            rtn_obj['msg'] = "It is not a right method!"
            rtn_obj['states'] = json_states
            data = json.dumps(rtn_obj)
            return HttpResponse(data)    
        else:
            rtn_obj['ack'] = "0"
            rtn_obj['msg'] = "states not exists!"
            data = json.dumps(rtn_obj)
            return HttpResponse(data)  
    else :
        rtn_obj['ack'] = "0"
        rtn_obj['msg'] = "It is not a right method!"
        data = json.dumps(rtn_obj)
        return HttpResponse(data)    
    
def content_email(subject,text,link,user_id,admin_id):    
    admin_info = get_user_details(admin_id)
    userinfo = get_user_details(user_id) 
    if link:
        edit_link = link
    else :
        edit_link = ""
    approval_track_mail=EmailTemplates.objects.get(pk=6) 
    t = Template(approval_track_mail.templatebody)
    c = Context({'approval_text' : text,'edit_link' : edit_link })
    msg_html = t.render(c)
    send_mail(subject, 'hello world again', admin_info.email, [userinfo.email], html_message=msg_html)

def get_user_details(user_id):    
    user = User.objects.get(pk=user_id) 
    return user