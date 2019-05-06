# -*- coding: utf-8 -*-
import scrapy
from distribute.views import *

class SdqtsSpider(scrapy.Spider):
    name = "sdqts"
    allowed_domains = ["www.sdqts.gov.cn"]
    start_urls = ['http://www.sdqts.gov.cn/sdzj/380936/index.html']

    def parse(self, response):
        sdqts_table = response.xpath('//*[@id="2d758f3ea2c041e399b5d84609a300f5"]/div[2]/div[2]/div[2]/table[2]/tbody/tr')
        for i in sdqts_table:
            sdqts_title = i.xpath('td/table/tbody/tr/td[1]/a/text()').extract_first()
            sdqts_date = i.xpath('td/table/tbody/tr/td[4]/text()').extract_first()
            sdqts_url = i.xpath('td/table/tbody/tr/td[1]/a/@href').extract_first()
            sdqts_url = set_url_head(sdqts_url,response.url)
            if sdqts_url:
                yield scrapy.Request(sdqts_url, callback=self.parse_item,meta={'sdqts_title':sdqts_title,'sdqts_date':sdqts_date,})

    def parse_item(self, response):
        sdqts_title = response.meta['sdqts_title']
        sdqts_date = response.meta['sdqts_date']
        tr = response.xpath('//div[@class="gov_infoCatalog_detailsection"]//table//tr')
        data = {}
        if len(tr) == 2:
            td_title = tr[0].xpath('td')
            td_val = tr[1].xpath('td')
            for i in range(0,len(tr[1].xpath('td'))):
                data[td_title[i].xpath('string(.)').extract_first()] = td_val[i].xpath('string(.)').extract_first()
        if data:
            sendData('sdqts',data,response.url)