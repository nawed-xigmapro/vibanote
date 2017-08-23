from django.shortcuts import render
from django.template import context,Context,Template
from django.http import HttpResponseRedirect
from adminpanel.models import *
from django.contrib import messages
from django.core.validators import validate_email
from django.core.mail import send_mail
from frontend.contollers.commonctrl import *
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_index(request):
    return render(request, 'frontend/home.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscribeNewsletter(request):
    if request.POST:
        newsletter_mail = request.POST.get('newsletter_mail')
        if NewsLetter.objects.filter(email=newsletter_mail).exists():
            messages.add_message(request, messages.ERROR, 'Email ID Exists!')   
        else :
            try:
                validate_email(newsletter_mail)
                newsletter = NewsLetter(
                    email = newsletter_mail
                )
                newsletter.save()
                admininfo = ns_get_user(1)
                register_mail=EmailTemplates.objects.get(pk=1) 
                t = Template(register_mail.templatebody)
                c = Context({'email': newsletter_mail})
                msg_html = t.render(c)
                send_mail(register_mail.subject, 'hello world again', admininfo.email, [admininfo.email,newsletter_mail], html_message=msg_html)
                messages.add_message(request, messages.SUCCESS, 'Successfully Subscribe!') 
            except:
                # not valid email
                messages.add_message(request, messages.ERROR, 'Not a valid email!')
           
        return HttpResponseRedirect('/') 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_cms(request,slug):
    if slug :
           if Cms.objects.filter(slug=slug).exists():
               slug_details = Cms.objects.get(slug=slug)
               title = slug_details.title
               #description = slug_details.text
               t = Template(slug_details.text)
               c = Context({})
               msg_html = t.render(c)
               return render(request,'frontend/cms.html',{ 'text' : msg_html, 'title' : title })
           else :
              return HttpResponseRedirect('/') 
    else:
      return HttpResponseRedirect('/')    
  
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def feedback_submit(request):
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        feedback_text = request.POST.get('feedback_text')
        try:
            validate_email(email)
        except validate_email.ValidationError:
            messages.add_message(request, messages.ERROR, 'Not a valid email!')  
            return HttpResponseRedirect('/')    # not valid email
                     
        obj_feedback = Feedback(
            name = name,
            email = email,
            contactno = contactno,
            feedback_text = feedback_text
        )
        obj_feedback.save()
        admininfo = ns_get_user(1)
        register_mail=EmailTemplates.objects.get(pk=5) 
        t = Template(register_mail.templatebody)
        c = Context({'name': name, 'email': email, 'contactno': contactno, 'feedback_text' : feedback_text})
        msg_html = t.render(c)
        send_mail('Vibanote Feedback', 'hello world again', admininfo.email, [admininfo.email], html_message=msg_html)
        messages.add_message(request, messages.SUCCESS, 'Feedback submitted!') 
        return HttpResponseRedirect('/')
        
           
           