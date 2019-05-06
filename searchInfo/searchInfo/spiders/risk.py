# -*- coding: utf-8 -*-
import scrapy
import urllib2
import json
# from distribute.views import sendData
# from datadeal.models import SpiderData
from searchInfo.items import FileItem
from scrapy.loader import ItemLoader

'''国家食药局风险检测文件爬虫'''
class RiskSpider(scrapy.Spider):
    name = "risk"
    allowed_domains = ["www.sda.gov.cn"]
    start_urls = ['http://www.sda.gov.cn/WS01/CL1667/index.html']

    def parse(self, response):
        # 食品
        url = 'http://www.sda.gov.cn/WS01/CL1667/index.html'
        yield scrapy.Request(url, callback=self.parse_item)
        # for i in range(1,222):
        #     url = 'http://www.sda.gov.cn/WS01/CL1667/index_%s.html' % i
        #     yield scrapy.Request(url, callback=self.parse_item)

        # 药品
        url = 'http://www.sda.gov.cn/WS01/CL1429/'
        yield scrapy.Request(url, callback=self.parse_item)
        # for i in range(1,12):
        #     url = 'http://www.sda.gov.cn/WS01/CL1429/index_%s.html' % i
        #     yield scrapy.Request(url, callback=self.parse_item)

        #化妆品
        url = 'http://www.sda.gov.cn/WS01/CL1866/'
        yield scrapy.Request(url, callback=self.parse_item)
        # for i in range(1,3):
        #     url = 'http://www.sda.gov.cn/WS01/CL1866/index_%s.html' % i
        #     yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        urls = response.xpath('/html/body/table[3]//tr/td[3]/table[2]//tr/td/table[1]//a')   
        for url in urls:
            text = url.xpath('string(.)').extract_first()
            if '不合格' in text or '抽检' in text:
                url = url.xpath('@href').extract_first().replace('..','')
                url = 'http://www.sda.gov.cn/WS01'+url
                yield scrapy.Request(url, callback=self.parse_detail)
    
    def parse_detail(self,response):
        path = response.xpath('//a')
        l = ItemLoader(item=FileItem(), response=response)
        for i in path:
            url = i.xpath('@href').extract_first()
            if url:
                if url.endswith('.doc') or url.endswith('.xlsx') or url.endswith('.xls') or url.endswith('.docx') or url.endswith('.rar') or url.endswith('.pdf') or url.endswith('.zip'):
                        url = 'http://www.sda.gov.cn'+url
                        l.add_value('file_urls',url)
        return l.load_item()