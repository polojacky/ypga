from django.conf.urls import patterns, url
from about import views

urlpatterns = patterns('',
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^$', views.index, name='index'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^copyright/$', views.copyright, name='copyright'),
    url(r'^externalLinks/$', views.external, name='external'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^lab/$', views.lab, name='lab'),
)