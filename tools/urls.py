from django.conf.urls import patterns, url
from tools import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^snp/download/$', views.snpDownload, name='snpDownload'),
    url(r'^snp/$', views.snp, name='snp'),
    url(r'^snpResult/$', views.snpResult, name='snpResult'),
    url(r'^snpView/(?P<id>[\w]+)/$', views.snpView, name='snpView'),
    url(r'^intergenic/$', views.intergenic, name='intergenic'),
    url(r'^intergenicResult/$', views.intergenicResult, name='intergenicResult'),
    url(r'^intergenic/download/$', views.intergenicDownload, name='intergenicDownload'),
    url(r'^intergenicView/(?P<id>[\w |\-_:]+)/$', views.intergenicView, name='intergenicView'),

    url(r'^homology/download/$', views.homologyDownload, name='homologyDownload'),
    url(r'^homology/$', views.homology, name='homology'),
    url(r'^homologyResult/$', views.homologyResult, name='homologyResult'),
    url(r'^homologyView/$', views.homologyView, name='homologyView'),
    url(r'^homologyViewNetwork/$', views.homologyViewNetwork, name='homologyViewNetwork'),
    url(r'^blastIndex/$', views.blastIndex, name='blastIndex'),
    url(r'^blast/$', views.blast, name='blast'),
    url(r'^blastResult/$', views.blastResult, name='blastResult'),
    url(r'^ajaxQueryState/$', views.ajaxQueryState, name='ajaxQueryState'),
)