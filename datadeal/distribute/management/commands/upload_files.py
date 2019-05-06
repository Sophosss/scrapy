#!coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from distribute.views import get_mac_address,HOST
from datadeal.settings import BASE_DIR
import requests
import os

class Command(BaseCommand):
    help = '上传本机medias下的下载文件至主机'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='spider_label', nargs='*',
            help='Specify the spider dir to upload.')

    def handle(self, *args, **options):
        dir_name = BASE_DIR+'/datadeal/medias'
        upload_files = {}
        files = os.listdir(dir_name)
        if len(args) > 0:
            dir_list = args
        else:
            dir_list = []
            for f in files:
                if not '.' in f:
                    dir_list.append(f)
        for d in dir_list:
            d_files = os.listdir(dir_name+'/'+d)
            for df in d_files:
                upload_files[d+'/'+df]=open(dir_name+'/'+d+'/'+df,'rb')
        url = HOST+'/upload_files/'
        response = requests.post(url,files=upload_files)
        print response.content.decode('utf8')