# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = [
  url(r'^create_node/$', CreateNode.as_view() ,name='create_node'),
  url(r'^get_spiders/$', getSpiders.as_view() ,name='get_spiders'),
  url(r'^handle_tasks/$', handleTasks.as_view() ,name='handle_tasks'),
  url(r'^over_tasks/$', overTasks.as_view() ,name='over_tasks'),
  url(r'^save_data/$', SaveData.as_view() ,name='save_data'),
  url(r'^get_spidername/$', GetSpiderName.as_view() ,name='get_spidername'),
]