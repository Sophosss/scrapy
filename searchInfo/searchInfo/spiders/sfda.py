# -*- coding: utf-8 -*-
import scrapy
import urllib
import urllib2
import bs4
from distribute.views import sendData
from datadeal.models import SpiderData

class SfdaSpider(scrapy.Spider):
    name = "sfda"
    allowed_domains = ["app1.sfda.gov.cn"]
    start_urls = ['http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=114&tableName=TABLE114&title=%E5%9B%BD%E5%AE%B6%E9%A3%9F%E5%93%81%E5%AE%89%E5%85%A8%E7%9B%91%E7%9D%A3%E6%8A%BD%E6%A3%80%EF%BC%88%E4%B8%8D%E5%90%88%E6%A0%BC%E4%BA%A7%E5%93%81%EF%BC%89&bcId=143106776907834761101199700381']

    def parse(self, response):
        # for i in range(1,238):
        for i in range(10,20):
            yield scrapy.FormRequest(
                url='http://app1.sfda.gov.cn/datasearch/face3/search.jsp',
                formdata={
                    "State":"1",
                    "bcId":"143106776907834761101199700381",
                    "curstart":str(i),
                    "tableId":"114",
                    "tableName":"TABLE114",
                    "viewsubTitleName":"COLUMN1486",
                    "viewtitleName":"COLUMN1490"
                },
                callback=self.after_post
            )

    def after_post(self, response):
        for a in response.xpath('//a'):
            aid = a.xpath('@href').extract_first().split('&Id=')[1].split('\'')[0]
            get_url = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=114&tableName=TABLE114&Id="+aid
            yield scrapy.Request(get_url, callback=self.parse_item)

    def parse_item(self, response):
        trs = response.xpath('//table/tr')
        data = {}
        for tr in trs:
            key = tr.xpath('td[1]/text()').extract_first()
            val = tr.xpath('td[2]/text()').extract_first()
            if key or val:
                data[key] = val
        try:
            already = SpiderData.objects.filter(scrapyname='sfda',data__contains={u"被抽样单位名称":data[u'被抽样单位名称'],u"生产日期/批号":data[u'生产日期/批号'],u"抽检项目":data[u'抽检项目']}).count()
        except:
            already = 1
        if not already:
            sendData('sfda',data,response.url)