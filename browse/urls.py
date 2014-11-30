from django.conf.urls import patterns, url
from browse import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    url(r'^genome/(?P<id>[\w]+)/$', views.genome, name='genome'),
    url(r'^gene/download/$', views.geneDownload, name='geneDownload'),
    url(r'^gene/$', views.geneAll, name='geneAll'),
    url(r'^gene/(?P<id>[\w]+)/$', views.gene, name='gene'),
    url(r'^geneDetail/(?P<id>[\w]+)/$', views.geneDetail, name='geneDetail'),
    url(r'^srna/download/$', views.srnaDownload, name='srnaDownload'),
    url(r'^srna/$', views.srnaAll, name='srnaAll'),
    url(r'^srna/(?P<id>[\w]+)/$', views.srna, name='srna'),
    url(r'^srnaDetail/(?P<id>[\w -:_|%]+)/$', views.srnaDetail, name='srnaDetail'),
    url(r'^exp/download/$', views.expDownload, name='expDownload'),
    url(r'^exp/$', views.expAll, name='expAll'),
    url(r'^exp/(?P<id>[\w]+)/$', views.exp, name='exp'),
    url(r'^expDetail/(?P<id>[\w]+)/$', views.expDetail, name='expDetail'),
)