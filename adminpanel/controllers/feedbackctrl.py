from django.template import context
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from django.db import connection
from django.utils import formats
from adminpanel.models import *
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
def list_feedbacks(request):
   if 'admin_id' in request.session:
        return render(request, 'adminpanel/list_feedback.html',{})
   else :
       return HttpResponseRedirect('/admin/login/')

def get_feedbacks(request):
        totalrows = Feedback.objects.count()
        cursor = connection.cursor()
        order = request.GET['order']

        if 'search' in request.GET and 'sort' not in request.GET :
         column_name = 'adminpanel_feedback.email'
         srch = request.GET['search']
         cursor.execute("select * from adminpanel_feedback where adminpanel_feedback.email like '"+srch+"%' or adminpanel_feedback.name like '"+srch+"%' ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' in request.GET :
            srch = request.GET['search']
            sort = request.GET['sort']
            if sort == "email":
                column_name = 'adminpanel_feedback.email'
            elif sort == "name":    
                column_name = 'adminpanel_feedback.name'
            else :
             column_name = 'adminpanel_feedback.id'

            if srch :
              cursor.execute("select * from adminpanel_feedback where adminpanel_feedback.email like '"+srch+"%' or adminpanel_feedback.name like '"+srch+"%' ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])
            else:
             cursor.execute("select * from adminpanel_feedback ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        elif 'sort' in request.GET and 'search' not in request.GET:
            sort = request.GET['sort']
            if sort == "email":
                column_name = 'adminpanel_feedback.email'
            elif sort == "name":    
                column_name = 'adminpanel_feedback.name'    
            else :
             column_name = 'adminpanel_feedback.id'

            cursor.execute("select * from adminpanel_feedback ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        else :
         order = "Desc"
         column_name = 'adminpanel_feedback.id'
         cursor.execute("select * from adminpanel_feedback ORDER BY "+column_name+" "+order+"  LIMIT "+request.GET['limit']+" OFFSET "+ request.GET['offset'])

        all_feedbacks = dictfetchall(cursor)
        docs_dict = {
            'total': totalrows,
            'rows': [{'id': all_feedback['id'],
                      'email': all_feedback['email'],
                      'name': all_feedback['name'],
                      'contactno': all_feedback['contactno'],
                      'deletefeedback': all_feedback['id'],
                      'replyfeedback': all_feedback['email'],
                      'details': all_feedback['id'],
                      } for all_feedback in all_feedbacks]
        }
        return JsonResponse(docs_dict)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def feedback_details(request,feedback_id):
    if 'admin_id' in request.session:
            feedback = Feedback.objects.get(pk=feedback_id)
            return render(request,'adminpanel/feedbackdetails.html', {'feedback': feedback })
    else :
       return HttpResponseRedirect('/admin/login/') 
   
def delete_feedback(request):  
    res_json = {}
    import json  
    if request.method == 'POST':
        feedback_id=request.POST['feedback_id']
        if Feedback.objects.filter(pk=int(feedback_id)).exists():
            Feedback.objects.filter(pk=int(feedback_id)).delete()
            c = Feedback.objects.filter(pk=int(feedback_id)).count()
            if c:
                #messages.add_message(request, messages.ERROR, 'Technical error!')
                res_json['ack'] = "0"
                res_json['msg'] = "Technical error"
                res_json['msg_type'] = "error"
                data = json.dumps(res_json)
                return HttpResponse(data)
            else:
                #messages.add_message(request, messages.SUCCESS, 'Feedback deleted successfully!')
                res_json['ack'] = "1"
                res_json['msg'] = "Feedback deleted successfully!"
                res_json['msg_type'] = "success"
                data = json.dumps(res_json)
                return HttpResponse(data)
        else:
            res_json['ack'] = "0"
            res_json['msg'] = "Feedback not exists!"
            res_json['msg_type'] = "error"
            data = json.dumps(res_json)
            return HttpResponse(data)
    else:
        res_json['ack'] = "0"
        res_json['msg'] = "Not the right method!"
        res_json['msg_type'] = "error"
        data = json.dumps(res_json)
        return HttpResponse(data)
 
       
