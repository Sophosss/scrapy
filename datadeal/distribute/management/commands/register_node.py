#!coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from distribute.views import get_mac_address,HOST
import urllib,urllib2
import json

class Command(BaseCommand):
    help = '注册节点mac地址'

    def handle(self, *args, **options):
        mac = get_mac_address()
        posturl = HOST+'/distribute/create_node/'
        data = {'uid':mac}
        data = urllib.urlencode(data)
        f = urllib2.urlopen(posturl,data)
        result = f.read().decode('utf8')
        print result