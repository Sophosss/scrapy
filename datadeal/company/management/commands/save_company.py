#!coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from company.models import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import urllib
import json

class Command(BaseCommand):
    help = '保存公司信息'

    def handle(self, *args, **options):
        company_list = ['新泰市人民药业有限公司仁德人民医药商场','新泰市人民药业有限公司新兰人民医药商场','新泰市人民药业有限公司黄崖人民医药商场','新泰市泉沟安康大药店','新泰市百姓园大药房','新泰市泉沟镇保安堂大药店','新泰市泉沟镇子恒药店','新泰市泉沟镇老百姓大药房','新泰市泉沟平价大药店','新泰市泉沟镇泉民大药店','新泰市康宇大药店','韩庄众心百姓大药房','西张庄众心百姓大药房','芙蓉街众心百姓大药房','淄博新华大药店连锁有限公司桓台陈庄药店','淄博新华大药店连锁有限公司兴桓药店','淄博丰祺医药有限公司云涛药店','桓台县索镇瑞康药店','桓台县城区信康药店','桓台县东壁大药店','淄博丰祺医药零售有限公司侯庄药店','淄博丰祺医药零售有限公司姜坊药店','果里镇福生堂药店','果里镇广生堂药店','淄博市临淄昊虹工贸有限公司','青岛啤酒股份有限公司青岛啤酒三厂','青岛北苑英徽家具有限公司','青岛平泰电子有限公司','青岛司玛特瑞进电子有限公司','青岛黄金铅锌开发有限公司','青岛长荣化工有限公司','东明县迪奥化工有限公司','东明元创化工有限公司','东明宏昌化工有限公司','东明欧宝板业有限公司','山东优一化工有限公司','东明凌宇化工有限公司','东明佳润化工有限公司']
        
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        desired_capabilities["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        )
        browser = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
        browser.maximize_window()

        for company in company_list:
            keyword = urllib.quote(company)
            browser.get('http://www.xizhi.com/search?wd=%s&type=all' % keyword)
            try:
                a = browser.find_element_by_xpath('/html/body/div[5]/div[1]/ul/li/div/div[2]/h3/a')
            except:
                a = ''
            if a:
                browser.get(a.get_attribute("href"))
                name = browser.find_element_by_xpath('/html/body/div[5]/div[1]/div[2]/h2/a').text
                print name
                div = browser.find_element_by_xpath('//*[@id="details-content"]/div[1]/div[1]/div')
                tds = div.find_elements_by_tag_name('td')
                aleady = Company.objects.filter(name=name)
                if not aleady.count():
                    obj = Company.objects.create(name=name,address=tds[25].text,creditcode=tds[1].text,registration=tds[3].text,organization=tds[5].text,kind=tds[7].text,status=tds[9].text,legalperson=tds[11].text,start_at=tds[13].text,capital=tds[15].text,deadline=tds[17].text,give_at=tds[19].text,webpage=tds[21].text,authority=tds[23].text,scope=tds[27].text)
                else:
                    obj = ''

                if obj:
                    div = browser.find_element_by_xpath('//*[@id="details-content"]/div[1]/div[2]')
                    trs = div.find_elements_by_tag_name('tr')
                    if len(trs) > 1:
                        for i,tr in enumerate(trs):
                            if i > 0:
                                tds = tr.find_elements_by_tag_name('td')
                                if tds[2].text:
                                    subcribe = tds[2].text.split('/')
                                    if len(subcribe) > 1:
                                        subcribe_money = subcribe[0]
                                        subcribe_date = subcribe[1]
                                    else:
                                        subcribe_money = subcribe[0]
                                        subcribe_date = ''
                                else:
                                    subcribe_money = ''
                                    subcribe_date = ''
                                if tds[3].text:
                                    real = tds[3].text.split('/')
                                    if len(real) > 1:
                                        real_money = real[0]
                                        real_date = real[1]
                                    else:
                                        real_money = real[0]
                                        real_date = ''
                                else:
                                    real_money = ''
                                    real_date = ''
                                try:
                                    Shareholders.objects.create(name=tds[0].text,kind=tds[1].text,subcribe_money=subcribe_money,subcribe_date=subcribe_date,real_money=real_money,real_date=real_date,company=obj)
                                except:
                                    Shareholders.objects.create(name=tds[0].text,kind=tds[1].text,subcribe_money=subcribe_money,real_money=real_money,company=obj)

                    div = browser.find_element_by_xpath('//*[@id="details-content"]/div[1]/div[3]')
                    lis = div.find_elements_by_tag_name('li')
                    if len(lis) > 0:
                        for li in lis:
                            key = li.find_element_by_class_name('lab').text.split(u'：')[0]
                            val = li.find_element_by_class_name('lab-in').text
                            Member.objects.create(name=val,kind=key,company=obj)

        browser.quit()
