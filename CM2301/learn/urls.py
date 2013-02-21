from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # /
    url(r'^$', 'learn.views.home', name='home'),
    url(r'^videos/$', 'learn.views.videos'),
    url(r'^videos/submit/$', 'learn.views.video_submit'),
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    #Lecture URL's
    url(r'^lectures/create/$', 'learn.views.lecture_create'),
)
