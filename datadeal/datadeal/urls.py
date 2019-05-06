# -*- coding: utf-8 -*-
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.views.static import serve
from datadeal import settings
from .views import *
import xadmin
xadmin.autodiscover()

urlpatterns = [
  url(r'^admin/', include(xadmin.site.urls)),
  url(r'^$', IndexView.as_view() ,name='index'),
  url(r'^list/$', ListFrameView.as_view() ,name='list'),
  url(r'^detail/$', DetailFrameView.as_view() ,name='detail'),
  url(r'^back_html/$', AjaxBackHtmlView.as_view() ,name='back_html'),
  url(r'^upload_files/$', UploadFilesView.as_view() ,name='upload_files'),
  url(r'^zip_files/$', ZipFilesView.as_view() ,name='zip_files'),
  url(r'^del_file/$', DeleteFilesView.as_view() ,name='del_file'),
  url(r'^distribute/',include('distribute.urls')),
  url(r'^medias/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
  url(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT}),
]