# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from keywords import get_keywords,save_keyword_index
from PIL import Image
import time
import urllib
import json
import os
import time

def reset_cookies(browser,listCookies):
    browser.delete_all_cookies()
    for cookie in listCookies:
        browser.add_cookie({
            'domain': cookie['domain'] if cookie['domain'].startswith('.') else '.'+cookie['domain'],
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expires': None
        })

def login(browser):
    name = browser.find_element_by_id("TANGRAM_12__userName")
    name.clear()
    name.send_keys("yourname")
    password = browser.find_element_by_id("TANGRAM_12__password")
    password.clear()
    password.send_keys("yourpassword")
    submit = browser.find_element_by_id('TANGRAM_12__submit').click()
    time.sleep(3)
    with open('baidu_cookies.json', 'w') as f:
        cookies = browser.get_cookies()
        cookies[0]['create_at'] = time.time()
        data = json.dumps(cookies)
        f.write(data)

def move_fuc(action,browser,keyword,x,y,k):
    # 模拟移动鼠标截图
    trend = browser.find_element_by_id("trend")
    action.move_to_element_with_offset(trend,x,y).perform()
    time.sleep(10)
    browser.save_screenshot('images/screenshot.png')
    # 根据需要元素裁图
    viewbox = browser.find_element_by_id("viewbox")
    date = browser.find_element_by_xpath('//*[@id="viewbox"]/div[1]/div[1]').text.split(' ')[0]
    left = viewbox.location['x']
    top = viewbox.location['y']
    right = viewbox.location['x'] + viewbox.size['width']
    bottom = viewbox.location['y'] + viewbox.size['height']
    im = Image.open('images/screenshot.png') 
    im = im.crop((left, top, right, bottom))
    image_name = 'images/baidu_%s_%s.png' % (keyword,date)
    im.save(image_name)
    time.sleep(1)

    # 调用ocr识别图像
    os.system('./zfOcr '+image_name)
    time.sleep(3)
    dir_name = os.path.dirname(os.path.abspath(__file__))+'/'
    if os.path.exists(dir_name+image_name+'.txt'):
        with open(image_name+'.txt','r') as f:
            num = int(f.read())
            data = {'keyword_id':k[0],'site':u'百度','keyword_type':k[2],'index_date':date,'index_value':num}
            save_keyword_index(data)
    else:
        print '%s.txt file not exist' % (image_name)
    # print date,num
    

if __name__ == '__main__':
    browser = webdriver.PhantomJS()
    try:
        browser.maximize_window()
        keyword_list = get_keywords()
        for k in keyword_list:
            keyword = k[1].decode('utf8')
            keyword = urllib.quote(keyword.encode('cp936'))
            try:
                browser.get('http://index.baidu.com/?tpl=trend&word=%s' % keyword)
                with open('baidu_cookies.json', 'r') as f:
                    listCookies = f.read()
                    if listCookies:
                        listCookies = json.loads(listCookies)
                        create_at = listCookies[0]['create_at']
                    else:
                        create_at = 0
                    if create_at == 0 or time.time() - create_at > 3600*5:
                        login(browser)
                    else:
                        reset_cookies(browser,listCookies)
                        browser.get('http://index.baidu.com/?tpl=trend&word=%s' % keyword)
                        time.sleep(5)
                try:
                    trend = browser.find_element_by_id("trend")
                except:
                    trend = ''
                if trend:
                    action = ActionChains(browser)
                    for i in range(0,30):
                        x = 30 + 42*i
                        if i == 29:
                            x = 1230
                        move_fuc(action,browser,keyword,x,150,k)
                else:
                    print '%s not find' % keyword
            except Exception, e:
                print keyword,unicode(e)
    except Exception, e:
        print unicode(e)
    finally:
        browser.quit()