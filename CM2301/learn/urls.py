from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # /
    url(r'^videos/$', 'learn.views.videos'),
    url(r'^videos/submit/$', 'learn.views.video_submit'),
)