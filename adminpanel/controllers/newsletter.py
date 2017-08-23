from django.template import context,Template,Context
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from django.db import connection
from django.utils import formats
from adminpanel.models import *
from django.views.decorators.cache import cache_control
from django.core.mail import send_mass_mail,send_mail
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
def list_newsletter(request):
   if 'admin_id' in request.session:
        return render(request, 'adminpanel/list_newsletter.html',{})
   else :
       return HttpResponseRedirect('/admin/login/')
   

def get_allnewsletter(request):
        totalrows = NewsLetter.objects.count()
        cursor = connection.cursor()
        order = request.GET['order']

        if 'search' in request.GET and 'sort' not in request.GET :
         column_name = 'adminpanel_newsletter.email'
         srch = request.GET['search']
         cursor.execute("select * from adminpanel_newsletter where adminpanel_newsletter.email like '"+srch+"%' ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' in request.GET :
            srch = request.GET['search']
            sort = request.GET['sort']
            if sort == "email":
                column_name = 'adminpanel_newsletter.email'
            else :
             column_name = 'adminpanel_newsletter.id'

            if srch :
              cursor.execute("select * from adminpanel_newsletter where adminpanel_newsletter.email like '"+srch+"%' ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])
            else:
             cursor.execute("select * from adminpanel_newsletter ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' not in request.GET:
            sort = request.GET['sort']
            if sort == "email":
                column_name = 'adminpanel_newsletter.email'
            else :
             column_name = 'adminpanel_newsletter.id'

            cursor.execute("select * from adminpanel_newsletter ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        else :
         column_name = 'adminpanel_newsletter.id'
         cursor.execute("select * from adminpanel_newsletter ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        all_newsletters = dictfetchall(cursor)
        docs_dict = {
            'total': totalrows,
            'rows': [{'id': all_newsletter['id'],
                      'email': all_newsletter['email'],
                      'subscribedate': formats.date_format(all_newsletter['created_date'], "Y-m-d"),
                      'unsubscribe': all_newsletter['id'],
                      } for all_newsletter in all_newsletters]
        }
        return JsonResponse(docs_dict)

 
def unsubscribe_users(request):
    if 'admin_id' in request.session:    
        if request.method == 'POST': 
            res_json = {}
            import json
            subscribe_id=request.POST['subscribe_id']
            if NewsLetter.objects.filter(pk=int(subscribe_id)).exists():
                NewsLetter.objects.filter(pk=int(subscribe_id)).delete()
                c = NewsLetter.objects.filter(pk=int(subscribe_id)).count()
                if c:
                    res_json['ack'] = "0"
                    res_json['msg'] = "Technical error"
                    res_json['msg_type'] = "error"
                    data = json.dumps(res_json)
                    #messages.add_message(request, messages.ERROR, 'Technical error!')
                    return HttpResponse(data)
                else:
                    res_json['ack'] = "1"
                    res_json['msg'] = "User unsubscribed"
                    res_json['msg_type'] = "success"
                    data = json.dumps(res_json)
                    #messages.add_message(request, messages.SUCCESS, 'User unsubscribed!')
                    return HttpResponse(data)
            else:
                res_json['ack'] = "0"
                res_json['msg'] = "Subscribeuser not exists"
                res_json['msg_type'] = "error"
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
    
def mass_mail_send(request):
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
            newsletters=NewsLetter.objects.all()
            admin_info = User.objects.get(pk=request.session['admin_id'])
            #tuples = tuple((subject,"", admin_info.email, [newsletter.email]) for newsletter in newsletters)
            #send_mass_mail(tuples,fail_silently=False)
            for newsletter in newsletters:
                recepient_list.append(newsletter.email)
            
            send_mail(subject,'Here is the message.',admin_info.email,recepient_list,fail_silently=False,html_message=msg_html)
    
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
