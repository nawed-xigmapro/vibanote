from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .import contollers

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', contollers.home.home_index, name='home_index'),
    #user routes
    url(r'^login/', contollers.users.login_user, name='login_user'),
    url(r'^signup/', contollers.users.register_user, name='register_user'),
    url(r'^logout/', contollers.users.logout_page, name='logout_page'),
    url(r'^forgotpassword/', contollers.users.forgot_password, name='forgot_password'),
    url(r'^forgotlink/(?P<forgot_id>\d+)/', contollers.users.forgot_link, name='forgot_link'),
    url(r'^resetpassword/', contollers.users.reset_password, name='reset_password'),
    url(r'^dashboard/', contollers.users.dashboard, name='dashboard'),
    url(r'^profile/', contollers.users.profile, name='profile'),
    url(r'^edit-profile/', contollers.users.profile_edit, name='profile_edit'),
    url(r'^upload-pic/', contollers.users.pic_upload, name='pic_upload'),
    url(r'^change-password/', contollers.users.change_password, name='change_password'),
    url(r'^artist-details/(?P<username>[-\w]+)/', contollers.users.artist_details, name='artist_details'),
    url(r'^add-browsed/', contollers.users.add_mostbrowsed, name='add_mostbrowsed'),
    url(r'^user-send-message/', contollers.users.user_send_message, name='user_send_message'),
    url(r'^show-messages/', contollers.users.show_messages, name='show_messages'),
    url(r'^sent-messages/', contollers.users.show_sent_messages, name='show_sent_messages'),
    url(r'^get-user-messages/', contollers.users.get_user_messages, name='get_user_messages'),
    url(r'^user-delete-thread', contollers.users.user_delete_thread, name='user_delete_thread'),
    url(r'^user-delete-message', contollers.users.user_delete_msg, name='user_delete_msg'),
    url(r'^user-read-thread', contollers.users.user_read_thread, name='user_read_thread'),
    # site routes
    url(r'^subscribe-newsletter/', contollers.home.subscribeNewsletter, name='subscribe_newsletter'),
    url(r'^cms/(?P<slug>[-\w]+)/', contollers.home.show_cms, name='show_cms'),
    url(r'^feedback-form/', contollers.home.feedback_submit, name='feedback_submit'),
    url(r'^contact/', contollers.contact.show_contactinfo, name='show_contactinfo'),
    #videoupload
    url(r'^videoupload/', contollers.videosctrl.upload_videos, name='upload_videos'),
    url(r'^pending-videos/', contollers.videosctrl.pending_videos, name='pending_videos'),
    url(r'^my-videos/', contollers.videosctrl.my_videos, name='my_videos'),
    url(r'^video-details/(?P<slug>[-\w]+)/', contollers.videosctrl.video_details, name='video_details'),
    url(r'^video-edit/', contollers.videosctrl.video_edit, name='video_edit'),
    url(r'^public-video-detail/(?P<videoslug>[-\w]+)/', contollers.videosctrl.public_video_detail, name='public_video_detail'),
    #trackupload
    url(r'^trackupload/', contollers.tracksctrl.upload_tracks, name='upload_tracks'),
    url(r'^pending-tracks/', contollers.tracksctrl.pending_tracks, name='pending_tracks'),
    url(r'^my-tracks/', contollers.tracksctrl.my_tracks, name='my_tracks'),
    url(r'^track-details/(?P<slug>[-\w]+)/', contollers.tracksctrl.track_details, name='track_details'),
    url(r'^track-edit/', contollers.tracksctrl.track_edit, name='track_edit'),
    url(r'^delete-singletrack/', contollers.tracksctrl.singletrack_delete, name='singletrack_delete'),
    url(r'^public-track-detail/(?P<trackslug>[-\w]+)/', contollers.tracksctrl.public_track_detail, name='public_track_detail'),
    #albumupload
    url(r'^add-album/', contollers.albumctrl.add_album, name='add_album'),
    url(r'^album-details/(?P<slug>[-\w]+)/', contollers.albumctrl.album_details, name='album_details'),
    url(r'^public-album-details/(?P<slug>[-\w]+)/', contollers.albumctrl.public_album_details, name='public_album_details'),
    url(r'^my-albums/', contollers.albumctrl.my_albums, name='my_albums'),
    url(r'^pending-albums/', contollers.albumctrl.user_pending_albums, name='user_pending_albums'),
    url(r'^public-album-tracks/', contollers.albumctrl.public_album_tracks, name='public_album_tracks'),
    url(r'^edit-album/', contollers.albumctrl.album_edit, name='album_edit'),
    #search
    url(r'^search-type/', contollers.searchctrl.search_type, name='search_type'),
    url(r'^search/(?P<search_type>[-\w]+)/(?P<search_id>[-\w]+)/(?P<searchtext>[-\w]+)/', contollers.searchctrl.search_all, name='search_all'),
    #likes
    url(r'^like-it/', contollers.likectrl.like_it, name='like_it'),
    #url(r'^user-likes/', contollers.likectrl.search_type, name='search_type'),
    #country-states
    url(r'^get-states/', contollers.commonctrl.get_states, name='get_states'),
    #explore routes
    url(r'^explore/', contollers.explorectrl.show_tracks_videos, name='show_tracks_videos'),
    url(r'^top-five/', contollers.explorectrl.fontend_topfive, name='fontend_topfive'),
    
    
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

