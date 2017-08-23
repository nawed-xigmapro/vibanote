from django import template
from django.template import Context, Template
import os.path
from django.contrib.auth.models import User
from django.db.models import Count
from adminpanel.models import Cms,Genre,Countries,States,Banner,Messages
from django.db import connection
register = template.Library()

@register.simple_tag
def cmsbyid(id):
  cms=Cms.objects.get(pk=id)  
  t = Template(cms.text)
  c = Context({})
  msg_html = t.render(c)
  return ({'text':msg_html,'pic':cms.picture,'slug':cms.slug})  

@register.simple_tag      
def show_footer_menu():
 all_cms = Cms.objects.all().order_by('id')[:3]
 return(all_cms)

@register.simple_tag      
def get_tags(my_string):
 my_list = my_string.split(",")
 return(my_list)

@register.simple_tag
def userdetails(userid):
    cursor = connection.cursor()
    cursor.execute("select auth_user.*,adminpanel_userprofile.* from auth_user INNER JOIN adminpanel_userprofile"
    " ON auth_user.id = adminpanel_userprofile.user_id where auth_user.id="+str(userid))  
    usr=query_to_dicts(cursor)
    return usr
@register.simple_tag
def get_templategenre():
    genre=Genre.objects.all()
    return genre

@register.simple_tag
def get_countries():
    countries=Countries.objects.all()
    return countries

@register.simple_tag
def get_statesbyid(country_id):
    states=States.objects.filter(country_id=country_id)
    return states

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

@register.simple_tag
def get_track(album_id):
    cursor = connection.cursor()
    cursor.execute("select atr.title as track_title, atr.track_file from adminpanel_tracks as atr where atr.album_id="+str(album_id)+" limit 1")  
    track=query_to_dicts(cursor)
    return track

@register.simple_tag      
def get_banner():
 banner = Banner.objects.get(pk=1)
 return(banner)

@register.simple_tag
def get_unread_msgcount(user_id):
    unread = Messages.objects.values('thread_id').annotate(total=Count('thread_id')).filter(touser_id=user_id,is_read_to=0).count()
    return unread