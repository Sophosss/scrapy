# -*- coding: utf-8 -*-
import scrapy
from distribute.views import set_url_head
from searchInfo.items import FileItem
from scrapy.loader import ItemLoader

class QingDaoSpider(scrapy.Spider):
    name = "qingdao"
    allowed_domains = ["sfda.qingdao.gov.cn"]
    start_urls = ['http://sfda.qingdao.gov.cn/n32205967/n32206400/index.html']

    def parse(self, response):
        data = []
        qingdao_div = response.xpath('//div[@id="listChangeDiv"]/ul/li')
        for i in qingdao_div:
            qingdao_url = i.xpath('a/@href').extract_first()
            qingdao_url = set_url_head(qingdao_url,response.url)
            if qingdao_url:
                yield scrapy.Request(qingdao_url, callback=self.parse_item)

    def parse_item(self, response):
        qingdao_detail = response.xpath('//div[@class="main_t"]//a')
        l = ItemLoader(item=FileItem(), response=response)
        for i in qingdao_detail:
            url = i.xpath('@href').extract_first()
            url = set_url_head(url,response.url)
            if url:
                l.add_value('file_urls',url)
        return l.load_item()