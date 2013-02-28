from django.conf.urls import patterns, include, url

uuid = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'

urlpatterns = patterns('',
    # /
    url(r'^$', 'learn.views.misc.home', name='home'),
    #url(r'^videos/$', 'learn.views.videos'),
    url(r'^videos/submit/$', 'learn.views.video.submit'),
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    
    #Video URL's
    url(r'^videos/$', 'learn.views.video.all'),
    url(r'^videos/(?P<video_id>%s)/$' % (uuid), 'learn.views.video.video'),
    url(r'^videos/(?P<video_id>%s)/serve/(.+)$' % (uuid), 'learn.views.video.serve'),
    url(r'^videos/create/$', 'learn.views.video.create'),
    

    #Module URL's
    url(r'^modules/%', 'learn.views.module.modules'),
    url(r'^modules/(?P<module_id>%s)/$' % (uuid), 'learn.views.module.module'),

    #Lecture URL's
    url(r'^lectures/create/$', 'learn.views.lecture.create'),
)
