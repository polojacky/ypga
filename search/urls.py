from django.conf.urls import patterns, url
from search import views

urlpatterns = patterns('',
	url(r'^preview/$', views.preview, name='preview'),
    url(r'^quick/$', views.quick, name='quick'),
    url(r'^gene/download/$', views.geneDownload, name='geneDownload'),
    url(r'^srna/download/$', views.srnaDownload, name='srnaDownload'),
    url(r'^exp/download/$', views.expDownload, name='expDownload'),
    url(r'^protein/download/$', views.proteinDownload, name='proteinDownload'),
    url(r'^snp/download/$', views.snpDownload, name='snpDownload'),
    url(r'^correspond/download/$', views.correspondDownload, name='correspondDownload'),
)