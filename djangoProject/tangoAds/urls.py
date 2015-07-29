from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^(\d+)/$', 'tangoAds.views.view_page', name='view_page'),
    url(r'^(\d+)/add_event$', 'tangoAds.views.add_event', name='add_event'),
    url(r'^new$', 'tangoAds.views.new_page', name='new_page'),
)
