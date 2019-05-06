# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from keywords import get_keywords,save_keyword_index
import re
import urllib
import time

if __name__ == '__main__':
    browser = webdriver.PhantomJS()
    try:
        keyword_list = get_keywords()
        for k in keyword_list:
            keyword = k[1].decode('utf8')
            keyword = urllib.quote(keyword.encode('utf8'))
            browser.get('http://zhishu.sogou.com/index/searchHeat?kwdNamesStr=%s&timePeriodType=MONTH&dataType=SEARCH_ALL&queryType=INPUT' % keyword)
            try:
                r = re.findall(r'root.SG.data = {"pvList":\[([\s\S]*)],"infoList"', browser.page_source, re.M)
            except:
                r = ''
            if r:
                points = eval(r[0].split('],"infoList"')[0])
                for p in points:
                    date = str(p['date'])
                    date = date[0:4]+'-'+date[4:6]+'-'+date[6:8]
                    # print date,p['pv']
                    data = {'keyword_id':k[0],'site':u'搜狗','keyword_type':k[2],'index_date':date,'index_value':p['pv']}
                    try:
                        save_keyword_index(data)
                    except Exception, e:
                        print unicode(e),keyword,date,p['pv']
            else:
                print '%s not find' % keyword
    except Exception, e:
        print unicode(e)
    finally:
        browser.quit()