# -*- coding: utf-8 -*-
import xadmin
from .models import *

class NodeAdmin(object):
    list_display = ['uid','status','ips','max_num']
    search_fields = ['uid']
    list_filter = ['status']
    list_editable = ['status']
xadmin.site.register(Node, NodeAdmin)

class NodeIpAdmin(object):
    list_display = ['ip','create_at']
    search_fields = ['ip']
    list_filter = ['create_at']
xadmin.site.register(NodeIp, NodeIpAdmin)

class NodeTaskAdmin(object):
    list_display = ['name','scrapy','priority','urls','status','create_at','get_at','over_at','node','nodeip']
    search_fields = ['name']
    list_filter = ['scrapy','node','status','get_at','over_at','create_at']
xadmin.site.register(NodeTask, NodeTaskAdmin)