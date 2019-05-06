# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import time

def write_fuc(browser):
    table = browser.find_element_by_xpath('//*[@id="mainleft"]')
    tag_a = table.find_elements_by_tag_name('a')
    with open('url_list.txt','a+') as f:
        for a in tag_a:
            text = a.text
            if u'信息公开表' in text:
                print text
                f.write(a.get_attribute("href")+'\n')

if __name__ == '__main__':
    
    # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    # desired_capabilities["phantomjs.page.settings.userAgent"] = (
    # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    # )
    browser = webdriver.PhantomJS()

    # browser.get('http://www.weihaifda.gov.cn/col/col14562/index.html')
    # browser.save_screenshot('screenshot.png')
    # write_fuc(browser)
    # browser.get('http://www.thsfda.gov.cn/xxgk/xzcfajxxgk/index_1.html')
    # write_fuc(browser)
    # for i in range(1,41):
    #     browser.get('http://ypjd.xjalt.gov.cn/qwssjgy.jsp?wbtreeid=1001&currentnum='+str(i)+'&newskeycode2=6KGM5pS%2F5aSE572a5qGI5Lu25L%2Bh5oGv5YWs5byA')
    #     write_fuc(browser)

    browser.get('http://www.huainan.gov.cn/public/column/4971284?type=4&catId=4977426&action=list')
    # browser.find_element_by_xpath('//*[@id="example"]/li[7]/div').click()
    # browser.switch_to.frame("conTarget")
    # write_fuc(browser)
    # time.sleep(1)
    # write_fuc(browser)

    count = 1
    while count <= 16:
        # try:
        # next_page = browser.find_element_by_xpath('//*[@id="container"]/div/div/table//tr/td[3]/div[2]/form/table//tr[21]/td/table//tr/td/table//tr/td[2]/div/a[7]')
        try:
            next_page = browser.find_element_by_partial_link_text('下一页')
            # next_page = browser.find_element_by_id('NextPage1_Next')
        except:
            next_page = ''
        # if 'default_pgNextDisabled' in next_page.get_attribute('class'):
        if not next_page:
            print 'enter_over'
            write_fuc(browser)
            break
        else:
            print 'enter'
            write_fuc(browser)
            next_page.click()
            time.sleep(2)
            count += 1
    browser.quit()
