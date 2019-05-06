# -*- coding: utf-8 -*-
import scrapy
from distribute.views import *

class XxgkSpider(scrapy.Spider):
    name = "xxgk"
    allowed_domains = ["xxgk.sdein.gov.cn"]

    def start_requests(self):
        results = getTasks('xxgk')
        self.taks_urls = {}
        self.tasks = {}
        if isinstance(results,dict):
            print results['error']
        else:
            for re in results:
                self.tasks[re['id']] = {'t_count':len(re['urls']),'count':0}
                for u in re['urls']:
                    self.taks_urls[u] = re['id']
                    yield self.make_requests_from_url(u)

    def after_parse(self,url):
        task_id = self.taks_urls[url]
        self.tasks[task_id]['count'] += 1
        if self.tasks[task_id]['count'] == self.tasks[task_id]['t_count']:
            afterTasks(task_id)

    def parse(self, response):
        xxgk_table = response.xpath('//table[@width="763"]/tr[4]/td/table/tr')
        for i in xxgk_table:
            sdein_title = i.xpath('td[2]/a/text()').extract_first()
            sdein_date = i.xpath('td[3]/text()').extract_first()
            sdein_url = i.xpath('td[2]/a/@href').extract_first()
            sdein_url = set_url_head(sdein_url,response.url)
            if sdein_url:
                yield scrapy.Request(sdein_url, callback=self.parse_item,meta={'sdein_title':sdein_title,'sdein_date':sdein_date,})
        self.after_parse(response.url)

    def parse_item(self, response):
        sdein_title = response.meta['sdein_title']
        sdein_date = response.meta['sdein_date']
        xxgk_content = response.xpath('/html/body/table[2]/tr[6]/td/table/tr[2]/td/table[4]/tr[3]/td/table[1]').xpath('string(.)').extract_first()
        trs = response.xpath('/html/body/table[2]/tr[6]/td/table/tr[2]/td/table[2]/tr')
        data = {}
        for tr in trs:
            tds = tr.xpath('td')
            for num,td in enumerate(tds):
                if num % 2 == 0:
                    data[td.xpath('string(.)').extract_first()] = tds[num+1].xpath('string(.)').extract_first()
        data['content'] = xxgk_content
        sendData('xxgk',data,response.url)