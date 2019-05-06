#!coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from datadeal.models import SpiderData

class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options): 
        # print SpiderData.objects(__raw__={'data.处罚结果（种类） ': '罚款 '})
        data = SpiderData.objects.filter(id=21475)
        # url_list = []
        # with open('d://project/commonscrapy/selenium/url_list.txt','r') as file:
        #     for line in file.readlines():
        #         if line.replace('\n',''):
        #             url_list.append(line.replace('\n',''))

        # for url in url_list:
        #     data = SpiderData.objects.filter(url=url)
        #     for d in data:
                
        #         print d.url
        #         d.delete()       
        for d in data:
            print d.data
            # for key,val in d.data.items():
            #     print key,val
