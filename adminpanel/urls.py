from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .import controllers

urlpatterns = [
    # user routes
    #url(r'^$', controllers.users.admin_login, name='admin_login'),
    url(r'^login/', controllers.users.admin_login, name='admin_login'),
    url(r'^logout/', controllers.users.admin_logout, name='admin_logout'),
    url(r'^artists/', controllers.users.artist_list, name='artist_list'),
    url(r'^all-artists/', controllers.users.get_artist_list, name='get_artist_list'),
    url(r'^userdetails/(?P<user_id>\d+)/', controllers.users.get_userdetails, name='get_userdetails'),
    url(r'^deactivateuser/', controllers.users.deactivate_users, name='deactivate_users'),
    url(r'^activateuser/', controllers.users.activate_users, name='activate_users'),
    url(r'^forgot-password/', controllers.users.forgotpasswordform, name='forgotpasswordform'),
    url(r'^forgotpassword/', controllers.users.forgot_password, name='forgot_password'),
    url(r'^forgotlink/(?P<forgot_id>\d+)/', controllers.users.forgot_link, name='forgot_link'),
    url(r'^resetpassword/', controllers.users.reset_password, name='reset_password'),
    url(r'^password-change', controllers.users.admin_change_password, name='admin_change_password'),
    url(r'^email-change', controllers.users.admin_change_email, name='admin_change_email'),
    url(r'^admin-user-edit', controllers.users.admin_user_edit, name='admin_user_edit'),
    url(r'^admin-user-picedit', controllers.users.admin_userpic_upload, name='admin_userpic_upload'),
    url(r'^admin-delete-users', controllers.users.admin_delete_users, name='admin_delete_users'),
    url(r'^admin-inbox-msg', controllers.users.admin_inbox_messages, name='admin_inbox_messages'),
    url(r'^admin-sent-msg', controllers.users.admin_outbox_messages, name='admin_outbox_messages'),
    url(r'^admin-delete-thread', controllers.users.admin_delete_thread, name='admin_delete_thread'),
    url(r'^admin-delete-message', controllers.users.admin_delete_msg, name='admin_delete_msg'),
    url(r'^admin-read-thread', controllers.users.admin_read_thread, name='admin_read_thread'),
    url(r'^thread-detail', controllers.users.get_thread_detail, name='get_thread_detail'),
    url(r'^user-send-message/', controllers.users.admin_user_send_message, name='admin_user_send_message'),
    url(r'^mass-mail-artists/', controllers.users.mass_mail_artists, name='mass_mail_artists'),
    # cms routes
    url(r'^cms/', controllers.cms.list_cms, name='list_cms'),
    url(r'^create-cms/', controllers.cms.create_cms, name='create_cms'),
    url(r'^edit-cms/', controllers.cms.edit_cms, name='edit_cms'),
    url(r'^cms-details/(?P<cms_id>\d+)/', controllers.cms.cms_details, name='cms_details'),
    url(r'^allcms/', controllers.cms.get_allcms, name='get_allcms'),
    #newsletter routes
    url(r'^newsletter/', controllers.newsletter.list_newsletter, name='list_newsletter'),
    url(r'^allnewsletter/', controllers.newsletter.get_allnewsletter, name='get_allnewsletter'),
    url(r'^unsubscribe-users/', controllers.newsletter.unsubscribe_users, name='unsubscribe_users'),
    url(r'^mass-mail-send/', controllers.newsletter.mass_mail_send, name='mass_mail_send'),
    #feedback routes
    url(r'^feedbacks/', controllers.feedbackctrl.list_feedbacks, name='list_feedbacks'),
    url(r'^allfeedback/', controllers.feedbackctrl.get_feedbacks, name='get_feedbacks'),
    url(r'^feedback-details/(?P<feedback_id>\d+)/', controllers.feedbackctrl.feedback_details, name='feedback_details'),
    url(r'^feedback-delete/', controllers.feedbackctrl.delete_feedback, name='delete_feedback'),
    #emailtemplates routes
    url(r'^email-templates/', controllers.email_templates.emailtemplates, name='emailtemplates'),
    url(r'^edit-emailtemplate/(?P<templateID>\d+)/', controllers.email_templates.edit_emailtemplates, name='edit_emailtemplates'),
    url(r'^edit-mailtemplate/', controllers.email_templates.edit_mailtemplate, name='edit_mailtemplate'),
    #contactinfo routes
    url(r'^editcontactinfo/', controllers.contactinfo.edit_contactdetails, name='edit_contactdetails'),
    url(r'^contactinfo/', controllers.contactinfo.contact_details, name='contact_details'),
    #genre routes
    url(r'^add-genre/', controllers.genrectrl.add_genre, name='add_genre'),
    url(r'^genre/', controllers.genrectrl.list_genre, name='list_genre'),
    url(r'^allgenre/', controllers.genrectrl.get_allgenre, name='get_allgenre'),
    url(r'^genre-details/(?P<id>\d+)/', controllers.genrectrl.genre_details, name='genre_details'),
    url(r'^edit-genre/', controllers.genrectrl.edit_genre, name='edit_genre'),
    #type routes
    url(r'^add-type/', controllers.typectrl.add_type, name='add_type'),
    url(r'^types/', controllers.typectrl.list_type, name='list_type'),
    url(r'^alltype/', controllers.typectrl.get_alltype, name='get_alltype'),
    url(r'^type-details/(?P<id>\d+)/', controllers.typectrl.type_details, name='type_details'),
    url(r'^edit-type/', controllers.typectrl.edit_type, name='edit_type'),
    #videoroutes
    url(r'^video-details/(?P<slug>[-\w]+)/', controllers.videosctrl.video_details, name='admin_video_details'),
    url(r'^pending-videos/$', controllers.videosctrl.get_pending_videos, name='pending_videos'),
    url(r'^pending-videos/(?P<likes_order>\w+)/$', controllers.videosctrl.get_pending_videos, name='pending_videos_order'),
    url(r'^user-pending-videos/(?P<userid>\d+)/$', controllers.videosctrl.user_pending_videos, name='user_pending_videos'),
    url(r'^user-pending-videos/(?P<userid>\d+)/(?P<likes_order>\w+)/$', controllers.videosctrl.user_pending_videos, name='user_pending_videos_order'),
    url(r'^videos/$', controllers.videosctrl.get_videos, name='videos'),
    url(r'^videos/(?P<likes_order>\w+)/$', controllers.videosctrl.get_videos, name='videos_order'),
    url(r'^user-videos/(?P<userid>\d+)/$', controllers.videosctrl.user_videos, name='user_videos'),
    url(r'^user-videos/(?P<userid>\d+)/(?P<likes_order>\w+)/$', controllers.videosctrl.user_videos, name='user_videos_order'),
    url(r'^video-edit/', controllers.videosctrl.video_edit, name='video_edit'),
    url(r'^delete-video/', controllers.videosctrl.video_delete, name='video_delete'),
    url(r'^approve-video/', controllers.videosctrl.video_approve, name='video_approve'),
    url(r'^disapprove-video/', controllers.videosctrl.video_disapprove, name='video_disapprove'),
    #trackroutes
    url(r'^track-details/(?P<slug>[-\w]+)/', controllers.tracksctrl.admin_track_details, name='admin_track_details'),
    url(r'^pending-tracks/$', controllers.tracksctrl.get_pending_tracks, name='get_pending_tracks'),
    url(r'^pending-tracks/(?P<likes_order>\w+)/$', controllers.tracksctrl.get_pending_tracks, name='get_pending_tracks_order'),
    url(r'^user-pending-tracks/(?P<userid>\d+)/$', controllers.tracksctrl.user_pending_tracks, name='user_pending_tracks'),
    url(r'^user-pending-tracks/(?P<userid>\d+)/(?P<likes_order>\w+)/$', controllers.tracksctrl.user_pending_tracks, name='user_pending_tracks_order'),
    url(r'^tracks/$', controllers.tracksctrl.get_tracks, name='get_tracks'),
    url(r'^tracks/(?P<likes_order>\w+)/$', controllers.tracksctrl.get_tracks, name='get_tracks_order'),
    url(r'^user-tracks/(?P<userid>\d+)/$', controllers.tracksctrl.user_tracks, name='user_tracks'),
    url(r'^user-tracks/(?P<userid>\d+)/(?P<likes_order>\w+)/$', controllers.tracksctrl.user_tracks, name='user_tracks_order'),
    url(r'^edit-track/', controllers.tracksctrl.admin_track_edit, name='admin_track_edit'),
    url(r'^delete-track/', controllers.tracksctrl.track_delete, name='track_delete'),
    url(r'^approve-track/', controllers.tracksctrl.track_approve, name='track_approve'),
    url(r'^disapprove-track/', controllers.tracksctrl.track_disapprove, name='track_disapprove'),
    #albumroutes
    url(r'^albums/$', controllers.albumctrl.albums_list, name='albums_list'),
    url(r'^albums/(?P<likes_order>\w+)/$', controllers.albumctrl.albums_list, name='albums_list_order'),
    url(r'^user-albums/(?P<userid>\d+)/$', controllers.albumctrl.user_albums_list, name='user_albums_list'),
    url(r'^user-albums/(?P<userid>\d+)/(?P<likes_order>\w+)/$', controllers.albumctrl.user_albums_list, name='user_albums_list_order'),
    url(r'^user-pending-albums/(?P<userid>\d+)/$', controllers.albumctrl.pending_albums_list, name='user_pending_albums_list'),
    url(r'^user-pending-albums/(?P<userid>\d+)/(?P<likes_order>\w+)/$', controllers.albumctrl.pending_albums_list, name='user_pending_albums_list_order'),
    url(r'^admin-pending-albums/$', controllers.albumctrl.pending_albums_list, name='pending_albums_list'),
    url(r'^admin-pending-albums/(?P<likes_order>\w+)/$', controllers.albumctrl.pending_albums_list, name='pending_albums_list_order'),
    url(r'^album-details/(?P<slug>[-\w]+)/', controllers.albumctrl.album_details, name='admin_album_details'),
    url(r'^album-edit/', controllers.albumctrl.album_edit, name='admin_album_edit'),
    url(r'^delete-album/', controllers.albumctrl.album_delete, name='album_delete'),
    url(r'^approve-album/', controllers.albumctrl.album_approve, name='album_approve'),
    url(r'^disapprove-album/', controllers.albumctrl.album_disapprove, name='album_disapprove'),
    
    #analyticsroutes
    url(r'^analytics-registration/', controllers.analyticsctrl.analytics_registration, name='analytics_registration'),
    url(r'^analytics-userstatus/', controllers.analyticsctrl.analytics_user_status, name='analytics_user_status'),
    url(r'^analytics-albums/', controllers.analyticsctrl.analytics_albumuploads, name='analytics_albumuploads'),
    url(r'^analytics-tracks/', controllers.analyticsctrl.analytics_trackuploads, name='analytics_trackuploads'),
    url(r'^analytics-videos/', controllers.analyticsctrl.analytics_videouploads, name='analytics_videouploads'),
    url(r'^customdates-users/', controllers.analyticsctrl.user_customdates, name='user_customdates'),
    url(r'^countrywise-users/', controllers.analyticsctrl.countrywise_users, name='countrywise_users'),
    url(r'^analytics-countries/', controllers.analyticsctrl.analytics_topcountries, name='analytics_topcountries'),
    url(r'^analytics-mostliked/', controllers.analyticsctrl.analytics_mostliked, name='analytics_mostliked'),
    url(r'^analytics-mostbrowsed/', controllers.analyticsctrl.analytics_mostbrowsed, name='analytics_mostbrowsed'),
    # banner routes
    url(r'^banner/', controllers.bannerctrl.list_banner, name='list_banner'),
    url(r'^add-banner/', controllers.bannerctrl.add_banner, name='add_banner'),
    url(r'^edit-banner/', controllers.bannerctrl.edit_banner, name='edit_banner'),
    url(r'^banner-details/(?P<banner_id>\d+)/', controllers.bannerctrl.banner_details, name='banner_details'),
    url(r'^all-banners/', controllers.bannerctrl.get_allbanner, name='get_allbanner'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)