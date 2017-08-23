from adminpanel.models import *
from django.http import HttpResponse
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

def ns_get_user(user_id):
    userinfo = User.objects.get(pk=user_id)
    return userinfo
    
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