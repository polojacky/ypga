from django.conf.urls import patterns, include, url
from settings import *
from filebrowser.sites import site

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ehf.views.home', name='home'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT, 'show_indexes': True}),
    url(r'^favicon\.ico$', 'django.views.generic.RedirectView', {'url': '/static/images/favicon.ico'}),
    url(r'^$', 'ypga.views.index'),
    url(r'^versionUpdate/$', 'ypga.views.versionUpdate'),

    url(r'^search/', include('search.urls', namespace="search")),
    url(r'^browse/', include('browse.urls', namespace="browse")),
    url(r'^download/', include('download.urls', namespace="download")),
    url(r'^about/', include('about.urls', namespace="about")),
    url(r'^tools/', include('tools.urls', namespace="tools")),
    url(r'^help/', include('help.urls', namespace="help")),
    url(r'^news/', include('news.urls', namespace="news")),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
