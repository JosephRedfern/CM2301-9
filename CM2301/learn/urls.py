from django.conf.urls import patterns, include, url
from learn.views.faq import *
from learn.views. announcement import *
from learn.views.module import *
from learn.views.announcement import *
from learn.views.management import *

uuid = '[a-f0-9]{8}[a-f0-9]{4}[a-f0-9]{4}[a-f0-9]{4}[a-f0-9]{12}'

urlpatterns = patterns('',
    # /
    url(r'^$', 'learn.views.misc.home', name='home'),
    #url(r'^videos/$', 'learn.views.videos'),
    url(r'^videos/submit/$', 'learn.views.video.submit'),
    url(r'^login/$', 'learn.views.misc.custom_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}),

    #management stuff
    url(r'^management/$', 'learn.views.management.overview'),

    url(r'^management/users$', UserListView.as_view()),
    url(r'^management/users/create$', UserCreateView.as_view()),
    url(r'^management/users/(?P<pk>%s)/update' % (uuid), UserUpdateView.as_view()),

    url(r'^management/courses$', CourseListView.as_view()),
    url(r'^management/courses/create', CourseCreateView.as_view()),
    url(r'^management/courses/(?P<pk>%s)/update' % (uuid), CourseUpdateView.as_view()),


    #Announcement Stuff
    url(r'^announcement/create/$', CreateAnnouncementView.as_view()),

    
    #Video URL's
    url(r'^videos/$', 'learn.views.video.all'),
    url(r'^videos/(?P<video_id>%s)/$' % (uuid), 'learn.views.video.video'),
    url(r'^videos/(?P<video_id>%s)/serve/(.+)$' % (uuid), 'learn.views.video.serve'),
    url(r'^videos/formats/(?P<video_format_id>%s)/serve/(.+)$' % (uuid), 'learn.views.video.format_serve'),
    url(r'^videos/create/$', 'learn.views.video.create'),
    url(r'^videos/(?P<video_id>%s)/progress/$' % (uuid), 'learn.views.video.conversion_progress'),
    url(r'^thumbnails/(?P<thumbnail_id>%s)/$' % (uuid), 'learn.views.video.thumbnail'),
        

    #Test URL's
    url(r'^tests/(?P<test_id>%s)/$'% (uuid), 'learn.views.test.test'),
    

    #Module URL's
    url(r'^modules/$', 'learn.views.module.modules'),
    url(r'^modules/create/$', CreateModuleView.as_view()),
    url(r'^modules/(?P<module_id>%s)/$' % (uuid), 'learn.views.module.module'),
    url(r'^modules/(?P<module_id>%s)/lectures/$' % (uuid), 'learn.views.module.lectures'),
    url(r'^modules/(?P<module_id>%s)/attachments/$' % (uuid), 'learn.views.module.attachments'),
    url(r'^modules/(?P<module_id>%s)/tests/$' % (uuid), 'learn.views.module.tests'),
    url(r'^modules/(?P<module_id>%s)/faqs/$' % (uuid), 'learn.views.faq.faqs'),
    url(r'^modules/(?P<module_id>%s)/faqs/ask/$' % (uuid), CreateFAQQuestionView.as_view()),
    url(r'^modules/(?P<module_id>%s)/faqs/(?P<faq_id>%s)/answer/$' % (uuid, uuid), CreateFAQAnswerView.as_view()),


    #Lecture URL's
    url(r'^modules/(?P<module_id>%s)/lectures/create/$' % (uuid), 'learn.views.lecture.create'),
    
    url(r'^lectures/create/$', 'learn.views.lecture.create'),
    url(r'^lectures/(?P<lecture_id>%s)/$' % (uuid), 'learn.views.lecture.view'),    
    
    #Attachment URL's
    url(r'^attachments/(?P<attachment_id>%s)/$' % (uuid), 'learn.views.attachment.attachment'),
    url(r'^attachments/(?P<attachment_id>%s)/download/$' % (uuid), 'learn.views.attachment.download_all_revisions'),
    url(r'^attachments/(?P<attachment_id>%s)/add/$' % (uuid), 'learn.views.attachment.revision_add'),
    url(r'^revisions/(?P<revision_id>%s)/$' % (uuid), 'learn.views.attachment.revision'),
    url(r'^revisions/(?P<revision_id>%s)/delete$' % (uuid), 'learn.views.attachment.revision_delete'),
    url(r'^revisions/(?P<revision_id>%s)/download/$' % (uuid), 'learn.views.attachment.revision_download'),
    url(r'^(.*)/(?P<object_id>%s)/attachments/download/$' % (uuid), 'learn.views.attachment.download_all_attachments'),
    url(r'^(.*)/(?P<object_id>%s)/attachments/create/$' % (uuid), 'learn.views.attachment.attachment_create'),
    
    #Test URL's
    url(r'^tests/(?P<test_id>%s)/$' % (uuid), 'learn.views.test.test'),
    url(r'^tests/$', 'learn.views.test.tests'),
    url(r'^results/(?P<test_instance_id>%s)/$' % (uuid), 'learn.views.test.test_results'),
    
)
