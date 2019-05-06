# -*- coding: utf-8 -*-
import scrapy
import urllib2
import json
from distribute.views import sendData
from datadeal.models import SpiderData

class BeiJingSpider(scrapy.Spider):
    name = "beijing"
    allowed_domains = ["www.bjda.gov.cn"]
    start_urls = ['http://www.bjda.gov.cn/eportal/ui?pageId=331216&currentPage=1&filter_LIKE_TITLE=&filter_LIKE_XKZH=']

    def parse(self, response):
        # for i in range(1,1472):
        for i in range(1,10):
            url = 'http://www.bjda.gov.cn/eportal/ui?pageId=331216&currentPage=%s&filter_LIKE_TITLE=&filter_LIKE_XKZH=' % i
            yield scrapy.Request(url, callback=self.parse_item)


    def parse_item(self, response):
        urls = response.xpath('//*[@id="form"]/div[2]/table//a')   
        for url in urls:
            text = url.xpath('string(.)').extract_first()
            if text and text == '查看':
                url = url.xpath('@href').extract_first()
                url = 'http://www.bjda.gov.cn'+url
                already = SpiderData.objects.filter(url=url)
                if already.count() == 0:
                    yield scrapy.Request(url, callback=self.parse_detail)
                else:
                    pass
                    # print 'already crawled'
    
    def parse_detail(self,response):
        trs = response.xpath('//*[@id="84f8b7f6cfc44b849b61b5c0ed21976a"]/div[2]/table//tr')
        data = {}
        for tr in trs:
            key = tr.xpath('th/text()').extract_first().replace(':','')
            val = tr.xpath('td/text()').extract_first()
            data[key] = val
        sendData('beijing',data,response.url) 