# -*- coding: utf-8 -*-
import scrapy
import urllib2
import json
from distribute.views import sendData
from datadeal.models import SpiderData
import json

class HaiNanSpider(scrapy.Spider):
    name = "hainan"
    allowed_domains = ["aj.hifda.gov.cn"]
    start_urls = ['http://aj.hifda.gov.cn/web/index.jsp']

    def parse(self, response):
        # for i in range(0,47):
        for i in range(0,5):
            yield scrapy.FormRequest(
                url='http://aj.hifda.gov.cn/loseCredit/refreshList.json',
                formdata={
                    "cityName":"",
                    "initialVal":"",
                    "ispublish":"1",
                    "listPageSize":"100",
                    "queryContent":"", 
                    "queryOrder":"0",
                    "searchOrderType":"0",
                    "selectIndex":"1",
                    "skip":"%s" % str(i*100),
                },
                callback=self.parse_item
            )

    def parse_item(self, response):
        result = json.loads(response.body)
        for r in result['resultData']:
            url = 'http://aj.hifda.gov.cn/web/showContent.jsp?id='+r['id']
            data = {u'企业（商户）名称':r['companyname'],u'注册地址':r['companysite'],u'法定代表人姓名':r['companyman'],u'法定代表人身份证号':r['companymanid'],u'负责人姓名':r['responsible_man'],u'负责人身份证号':r['resp_man_id'],u'直接责任人':r['direct_person'],u'社会信用代码':r['idcode'],u'案件分类':r['toclassify'],u'案件名称':r['losecase'],u'行政处罚决定文书号':r['punish_writ_num'],u'主要违法事实':r['losedetail'],u'处罚依据和内容':r['punishway'],u'处罚机关':r['punishunit'],u'处罚时间':r['punishtime']}
            already = SpiderData.objects.filter(url=url)
            if already.count() == 0:
                sendData('hainan',data,url)
            else:
                pass
                # print 'already crawled'