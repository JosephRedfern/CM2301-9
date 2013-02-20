from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # /
    #url(r'^$', 'learn.views.home', name='home'),
    url(r'^$', 'learn.views.current_datetime', name='current_datetime'),
)
