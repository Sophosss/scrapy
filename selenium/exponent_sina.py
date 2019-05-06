# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from keywords import get_keywords,save_keyword_index
import urllib
import time
import sys

def move_fuc(action,element,browser,x,y=200):
    action.move_to_element_with_offset(element,x,y).perform()
    time.sleep(1)
    div = browser.find_element_by_xpath('//*[@id="hotword_chart"]/div/div[2]')
    text = div.get_attribute('innerHTML')
    date = text.split('<br>')[0].split(u'：')[1]
    val = text.split('<br>')[1].split(u'：')[1].replace(',','')
    return date,val


if __name__ == '__main__':
    browser = webdriver.PhantomJS()
    try:
        browser.maximize_window()
        keyword_list = get_keywords()
        for k in keyword_list:
            keyword = k[1].decode('utf8')
            keyword = urllib.quote(keyword.encode('utf8'))
            browser.get('http://data.weibo.com/index/hotword?wid=1020000010045&wname=%s' % keyword)
            try:
                canvas = browser.find_element_by_xpath('//*[@id="hotword_chart"]/div/canvas[7]')
            except:
                canvas = ''

            if canvas:
                action = ActionChains(browser)

                data = {}
                for i in range(0,33):
                    date,val = move_fuc(action,canvas,browser,35+i*26)
                    # print date,val
                    data = {'keyword_id':k[0],'site':u'新浪','keyword_type':k[2],'index_date':date,'index_value':val}
                    try:
                        save_keyword_index(data)
                    except Exception, e:
                        print keyword,date,val,unicode(e)
            else:
                print '%s not find' % keyword
    except Exception, e:
        print unicode(e)
    finally:
        browser.quit()
