#!coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from distribute.views import get_mac_address,HOST
from datadeal.settings import BASE_DIR
import urllib,urllib2
import json
import os

class Command(BaseCommand):
    help = '开始爬取数据'

    def handle(self, *args, **options):
        posturl = HOST+'/distribute/get_spidername/'
        data = {}
        data = urllib.urlencode(data)
        f = urllib2.urlopen(posturl,data)
        result = f.read().decode('utf8')
        if result:
            os.system('cd %s/../searchInfo&&scrapy crawl %s' % (BASE_DIR,result))
        else:
            print u'暂时没有可执行任务'