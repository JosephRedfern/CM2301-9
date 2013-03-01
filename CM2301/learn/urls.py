from django.conf.urls import patterns, include, url

uuid = '[a-f0-9]{8}[a-f0-9]{4}[a-f0-9]{4}[a-f0-9]{4}[a-f0-9]{12}'

urlpatterns = patterns('',
    # /
    url(r'^$', 'learn.views.misc.home', name='home'),
    #url(r'^videos/$', 'learn.views.videos'),
    url(r'^videos/submit/$', 'learn.views.video.submit'),
    url(r'^login/$', 'learn.views.misc.custom_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    
    #Video URL's
    url(r'^videos/$', 'learn.views.video.all'),
    url(r'^videos/(?P<video_id>%s)/$' % (uuid), 'learn.views.video.video'),
    url(r'^videos/(?P<video_id>%s)/serve/(.+)$' % (uuid), 'learn.views.video.serve'),
    url(r'^videos/create/$', 'learn.views.video.create'),
    

    #Module URL's
    url(r'^modules/$', 'learn.views.module.modules'),
    url(r'^modules/(?P<module_id>%s)/$' % (uuid), 'learn.views.module.module'),

    #Lecture URL's
    url(r'^lectures/create/$', 'learn.views.lecture.create'),
    url(r'^lectures/(?P<lecture_id>%s)/$' % (uuid), 'learn.views.lecture.view'),    
    
    #Attachment URL's
    url(r'^attachments/(?P<attachment_id>%s)/$' % (uuid), 'learn.views.attachment.attachment'),
    url(r'^revisions/(?P<revision_id>%s)/$' % (uuid), 'learn.views.attachment.revision'),
    url(r'^revisions/(?P<revision_id>%s)/delete$' % (uuid), 'learn.views.attachment.revision_delete'),
    url(r'^revisions/(?P<revision_id>%s)/download' % (uuid), 'learn.views.attachment.revision_download'),
)
