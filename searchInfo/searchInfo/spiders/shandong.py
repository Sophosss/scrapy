# -*- coding: utf-8 -*-
import scrapy
from distribute.views import set_url_head
from searchInfo.items import FileItem
from scrapy.loader import ItemLoader

class shandongSpider(scrapy.Spider):
    name = "shandong"
    allowed_domains = ["www.creditsd.gov.cn"]
    start_urls = ['http://www.creditsd.gov.cn/creditsearch.punishmentList.phtml?id=']

    def parse(self, response):
        for i in range(1,11):
            url = 'http://www.creditsd.gov.cn/creditsearch.punishmentList.phtml?id=&keyword=&page=%s' % i
            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):
        div = response.xpath('/html/body/div/table[2]//tr')
        for i in div:
            url = i.xpath('td[1]/a/@href').extract_first()
            if url:
                url = 'http://www.creditsd.gov.cn'+url
                yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        img_url = response.xpath('//*[@id="img"]/@src').extract_first()
        if img_url:
            img_url = 'http://www.creditsd.gov.cn'+img_url
            l = ItemLoader(item=FileItem(), response=response)
            l.add_value('file_urls',img_url)
            return l.load_item()