#coding:utf8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

porxy_list = ['183.222.102.105','183.222.102.101','60.216.42.11','47.52.24.117']

proxy = Proxy(
    {
        'proxyType': ProxyType.MANUAL,
        'httpProxy': '47.52.24.117'
    }
)
desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
proxy.add_to_capabilities(desired_capabilities)
desired_capabilities["phantomjs.page.settings.userAgent"] = (
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
)

browser = webdriver.PhantomJS(desired_capabilities=desired_capabilities)

# browser.get('http://www.seabay.cn/cn/code/?search=pvg')
# print 'start_____'
# table = browser.find_element_by_xpath('//*[@id="infoiata"]')
# print table.get_attribute('innerHTML')
# browser.quit()


# browser.get('https://httpbin.org/get?show_env=1')            #检测头信息
browser.get('http://www.ip181.com/')                           #检测代理类型
# browser.get('http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+3+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E8%A1%8C%E6%94%BF%E6%A1%88%E4%BB%B6')
# browser.get('http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=114&tableName=TABLE114&title=%E5%9B%BD%E5%AE%B6%E9%A3%9F%E5%93%81%E5%AE%89%E5%85%A8%E7%9B%91%E7%9D%A3%E6%8A%BD%E6%A3%80%EF%BC%88%E4%B8%8D%E5%90%88%E6%A0%BC%E4%BA%A7%E5%93%81%EF%BC%89&bcId=143106776907834761101199700381')
# print 'start_____'
try:
    # browser.get('http://www.luan.gov.cn/opennessTarget/?branch_id=5212bc2d682e09147c7c4aa8&branch_type=&column_code=70302&topic_id=&tag=&page=1')
    # time.sleep(3)
    browser.save_screenshot('screenshot1.png')
    # print browser.page_source
    # WebDriverWait(browser,30).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,'.dataItem')))
    # resultlist = browser.find_element_by_id('list')
    # print resultlist.get_attribute('innerHTML')
    # time.sleep(10)
    # resultlist = browser.find_element_by_id('list')
    resultlist = browser.find_element_by_class_name('panel-body')
    print resultlist.get_attribute('innerHTML')
    # print browser.page_source
    # with open('wenshu.html','w') as ws:
    #     ws.write(resultlist.get_attribute('innerHTML'))
    # browser.save_screenshot('screenshot.png')
finally:
    browser.quit()