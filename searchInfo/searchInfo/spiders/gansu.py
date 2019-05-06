# -*- coding: utf-8 -*-
import scrapy
import urllib2
import json
from distribute.views import sendData
from datadeal.models import SpiderData

class GanSuSpider(scrapy.Spider):
    name = "gansu"
    allowed_domains = ["www.gsfda.gov.cn"]
    start_urls = ['http://www.gsfda.gov.cn:2180/xzlaw/xzlawActionWZ!list.do?queryBean.pn=1&queryBean.pageSize=100']

    def parse(self, response):
        # for i in range(1,106):
        for i in range(1,5):
            url = 'http://www.gsfda.gov.cn:2180/xzlaw/xzlawActionWZ!list.do?queryBean.pn=%s&queryBean.pageSize=100' % i
            yield scrapy.Request(url, callback=self.parse_item)


    def parse_item(self, response):
        urls = response.xpath('//*[@id="list"]//a')
        for url in urls:
            text = url.xpath('string(.)').extract_first()
            if text and text == '[查看]':
                url = url.xpath('@href').extract_first()
                url = 'http://www.gsfda.gov.cn:2180/xzlaw/'+url
                already = SpiderData.objects.filter(url=url)
                if already.count() == 0:
                    yield scrapy.Request(url, callback=self.parse_detail)
                else:
                    # print 'already crawled'
                    pass
    
    def parse_detail(self,response):
        trs = response.xpath('//*[@id="edit"]//tr')
        data = {}
        for i,tr in enumerate(trs):
            if i > 0:
                key = tr.xpath('th/text()').extract_first()
                val = val = tr.xpath('td/text()').extract_first()
                if key:
                    key = key.replace(':','').replace(' ','')
                    if not val:
                        val = ''
                    data[key] = val
        sendData('gansu',data,response.url) 