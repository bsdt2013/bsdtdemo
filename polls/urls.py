from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('polls.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<poll_key>\d+)/$', 'detail'),
    url(r'^(?P<poll_key>\d+)/results/$', 'results'),
    url(r'^(?P<poll_key>\d+)/vote/$', 'vote'),
)
