from django.template import context
from django.shortcuts import render
from django.http import HttpResponseRedirect
from adminpanel.models import *
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def emailtemplates(request):
   if 'admin_id' in request.session:
    emailtemplates = EmailTemplates.objects.all()
    return render(request,'adminpanel/email-templates.html',{'emailtemplates' : emailtemplates })
   else :
    return HttpResponseRedirect('/admin/login/') 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_emailtemplates(request,templateID):
    if 'admin_id' in request.session:
        emailtemplate = EmailTemplates.objects.get(pk=templateID)
        return render(request,'adminpanel/email-templatesdetails.html',{'emailtemplate' : emailtemplate })
    else :
     return HttpResponseRedirect('/admin/login/') 
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_mailtemplate(request):
    if request.POST :
        template_id = request.POST.get('template_id')
        template_title = request.POST.get('template_title')
        template_subject = request.POST.get('template_subject')
        template_body = request.POST.get('template_body')
        
        emailtemplate = EmailTemplates.objects.get(pk=template_id)
        emailtemplate.templatename=template_title
        emailtemplate.templatebody=template_body
        emailtemplate.subject=template_subject
        emailtemplate.save() 
        return HttpResponseRedirect('/admin/edit-emailtemplate/'+template_id+'/')
    else :
        return HttpResponseRedirect('/admin/login/')