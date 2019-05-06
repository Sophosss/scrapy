#!coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from datadeal.models import scrapyList,DataAlarm,SpiderData
import datetime

class Command(BaseCommand):
    help = '生成爬虫预警'

    def handle(self, *args, **options):
        scrapy = scrapyList.objects.filter(is_open=True)
        for s in scrapy:
            try:
                data = SpiderData.objects.filter(scrapyname=s.name).order_by('-create_at')[0]
            except:
                data = ''
            if data:
                nodata_day = (datetime.datetime.now()-data.create_at).days
                if nodata_day > s.alarm_day:
                    da = DataAlarm.objects.filter(is_alarm=True,scrapyname=s.name).order_by('-create_at')
                    if da.count():
                        alreay_day = (datetime.datetime.now()-da[0].create_at).days
                        if alreay_day > s.alarm_day:
                            DataAlarm.objects.create(scrapyname=s.name,is_alarm=True,remark='')
                    else:
                        DataAlarm.objects.create(scrapyname=s.name,is_alarm=True,remark='')