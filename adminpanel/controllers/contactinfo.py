from django.template import context
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from adminpanel.models import *
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contact_details(request):
    if 'admin_id' in request.session:
        if ContactInfo.objects.filter(pk=1).exists():
           contactinfo=ContactInfo.objects.get(pk=1)
           return render(request,'adminpanel/edit_contactinfo.html',{'contactinfo': contactinfo })
        else :
            return HttpResponseRedirect('/admin/artists/')
    else :
       return HttpResponseRedirect('/admin/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_contactdetails(request):
    if request.method == 'POST' and 'btn_edit' in request.POST :
       import re
       email = request.POST.get('email','NONE')
       address = request.POST.get('address','NONE')
       phone = request.POST.get('phone','NONE')
       contact_info_id = request.POST.get('contact_info_id','NONE')
       
       contactinfo_edit=ContactInfo.objects.get(pk=int(contact_info_id))
       contactinfo_edit.email=email
       contactinfo_edit.address=address
       contactinfo_edit.phone = phone
       contactinfo_edit.save()
       
       return HttpResponseRedirect('/admin/contactinfo/')
    
    else :
       return HttpResponseRedirect('/admin/login/')   





 
       
