#!coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from distribute.views import get_mac_address,HOST
from datadeal.settings import BASE_DIR
import urllib,urllib2
import json

class Command(BaseCommand):
    help = '同步主机spider文件'

    def handle(self, *args, **options):
        mac = get_mac_address()
        posturl = HOST+'/distribute/get_spiders/'
        data = {'uid':mac}
        data = urllib.urlencode(data)
        f = urllib2.urlopen(posturl,data)
        result = json.loads(f.read())

        if result.has_key('error'):
            print result['error']
        else:
            for key,val in result.items():
                with open(BASE_DIR+'/../searchInfo/searchInfo/spiders/'+key,'w') as s_file:
                    s_file.write(val)
            print u'同步完成'