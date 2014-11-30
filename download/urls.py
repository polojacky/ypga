from django.conf.urls import patterns, url

from download import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='download'),
    url(r'^register/$', views.register, name='register'),
    url(r'^downloadAll/$', views.downloadAll, name='downloadAll'),
    url(r'^gencsv/$', views.gencsv, name='gencsv'),
)