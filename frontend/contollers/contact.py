from django.shortcuts import render
from django.template import context
from adminpanel.models import *
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_contactinfo(request):
    contactinfo = ContactInfo.objects.get(pk=1)
    return render(request,'frontend/contactus.html',{'contactinfo': contactinfo })
    