# -*- coding: utf-8 -*-
import scrapy
import urllib2
import json
from distribute.views import sendData
from datadeal.models import SpiderData

'''山东省行政处罚案件爬虫'''
class CaseSpider(scrapy.Spider):
    name = "case"
    allowed_domains = ["sdlf.shandongbusiness.gov.cn"]
    start_urls = ['http://sdlf.shandongbusiness.gov.cn/newslist.shtml?method=listXzcf']

    def parse(self, response):
        for i in range(1,6):
            yield scrapy.FormRequest(
                url='http://sdlf.shandongbusiness.gov.cn/newslist.shtml',
                formdata={'pager.requestPage': str(i), 'method': 'listXzcf'},
                callback=self.after_post
            )

    def after_post(self, response):
        li = response.xpath('//ul[@class="rlistul"]/li')
        for l in li:
            date = l.xpath('span/text()').extract_first()
            title = l.xpath('a/text()').extract_first()
            url = 'http://sdlf.shandongbusiness.gov.cn'+l.xpath('a/@href').extract_first()
            yield scrapy.Request(url, callback=self.parse_item,meta={'date':date,'title':title})

    def parse_item(self, response):
        date = response.meta['date']
        title = response.meta['title']
        data = {}
        tables = response.xpath('//table[@class="rtab2"]')
        for table in tables:
            trs = table.xpath('tr')
            for tr in trs:
                key = tr.xpath('th/text()').extract_first().split(u'：')[0]
                value = tr.xpath('td/text()').extract_first()
                data[key] = value

        already = SpiderData.objects.filter(url=response.url)
        if already.count() == 0:
            sendData('case',data,response.url)
        else:
            pass
            # print 'already crawl'