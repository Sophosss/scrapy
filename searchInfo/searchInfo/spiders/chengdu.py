# -*- coding: utf-8 -*-
import scrapy
import urllib2
import json
from distribute.views import sendData
from datadeal.models import SpiderData

class ChengDuSpider(scrapy.Spider):
    name = "chengdu"
    allowed_domains = ["www.shfda.gov.cn"]
    start_urls = ['http://www.cdepb.gov.cn/cdepbws/Web/Template/GovDefaultList.aspx?cid=843']

    def parse(self, response):
        # for i in range(1,37):
        for i in range(1,10):
            url = 'http://www.shfda.gov.cn/XingZhengChuFa/xxgk2.aspx?pu=&qymc=&slrqstart=&slrqend=&pageindex=%s&pagesize=20' % i
            yield scrapy.Request(url, callback=self.parse_item)


    def parse_item(self, response):
        urls = response.xpath('//*[@id="b1"]//a')   
        for url in urls:
            text = url.xpath('string(.)').extract_first()
            if text and text == '详情':
                url = url.xpath('@href').extract_first()
                url = 'http://www.shfda.gov.cn/XingZhengChuFa/'+url
                already = SpiderData.objects.filter(url=url)
                if already.count() == 0:
                    yield scrapy.Request(url, callback=self.parse_detail)
                else:
                    # print 'already crawled'
                    pass
    
    def parse_detail(self,response):
        trs = response.xpath('//*[@id="main"]/div/div[2]/table//tr')
        data = {}
        for tr in trs:
            key = tr.xpath('td[1]/text()').extract_first()
            val = tr.xpath('td[2]/text()').extract_first()
            data[key] = val
        sendData('shanghai',data,response.url) 