from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # /
    url(r'^$', 'learn.views.home', name='home'),
)