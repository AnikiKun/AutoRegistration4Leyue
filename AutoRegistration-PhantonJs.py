#coding: utf-8

import time, threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyquery import PyQuery as pq

dcap = dict(DesiredCapabilities.PHANTOMJS)

class LeyueRegistration(object):

    def __init__(self):
        self.userName = 'xxxx'
        self.password = 'xxxx'
        self.host = 'http://portal.leyue100.com'
        self.cookies = []

    def loginFlow(self, driver):
        print(u'执行登录')
        loginUrl = 'http://portal.leyue100.com/aw/user/pwlogin'
        driver.get(loginUrl)
        # goLogin = driver.find_element_by_xpath('/html/body/div[2]/span/a')
        # goLogin.click()
        userInput = driver.find_element_by_id('login-username')
        userInput.send_keys(self.userName)
        passwordInput = driver.find_element_by_id('login-password')
        passwordInput.send_keys(self.password)
        driver.find_element_by_id('login-submit').click()
        driver.find_element_by_xpath('/html/body/div[1]/a/p')
        self.cookies = driver.get_cookies()
        print(u'登录成功')

    def waitLoading(self, driver):
        ajaxLoad = driver.find_element_by_class_name('ajaxload').get_attribute('style')
        loadNum = 0
        while 'none' not in ajaxLoad:
            time.sleep(1)
            loadNum += 1
            print(u'页面加载中...已等待 {} 秒'.format(loadNum))
            if loadNum >= 60:
                print(u'页面加载超时，正在尝试刷新当前页面后重试...')
                driver.refresh()
                loadNum = 0
            ajaxLoad = driver.find_element_by_class_name('ajaxload').get_attribute('style')

        print(u'页面请求加载完成...')

    def start(self):
        driver = webdriver.PhantomJS()
        driver.implicitly_wait(180)
        url = 'http://portal.leyue100.com/aw/registered/doctor?hid=d7YJg9tdDbH&dmid=9hyC7U37fSs&date=2018-02-17&did=4RTLjbCxUIt'
        # url = 'http://portal.leyue100.com/normal/registered/doctor?did=4RTLjbCxUIt&wid=6ViEjVnz5Uf&date=2018-02-03&dmid=c7ZtBTTpYxy'
        self.loginFlow(driver)
        # url = 'http://portal.leyue100.com/aw/registered/doctor?did=bwaFnvmcLAh&hid=d7YJg9tdDbH&date=2017-12-26&dmid=27ref6QNt2N'
        driver.get(url)
        self.waitLoading(driver)
        tryNum = 1
        doc = pq(driver.page_source)
        while len(doc('.dortor_list').find('.zanwu')) > 0:
            print(u"第{}次尝试获取挂号信息".format(tryNum))
            print(u'暂未刷出挂号信息，2秒后重试')
            time.sleep(2)
            print(u'刷新页面中...')
            driver.refresh()
            self.waitLoading(driver)
            # orderList = driver.find_elements_by_xpath('//div[@class="dortor_list"]/ul/li/span/a')
            tryNum += 1
        orderList = driver.find_elements_by_xpath('//div[@class="dortor_list"]/ul/li')
        print(u'成功刷到挂号信息！！总共号数 {} 个'.format(len(orderList)))
        print(u'开始尝试挂号！')
        for ol in orderList:
            hPath = self.host+ol.get_attribute('onclick')[22:-1]
            t = threading.Thread(target=self.tryGua, args=(hPath,ol.text,))
            # t.setDaemon(True)
            t.start()
            time.sleep(1)


    def tryGua(self, url, name):
        dcap["phantomjs.page.settings.userAgent"] = (
            u"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 {}".format(name)
        )
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
        driver.set_window_size(800, 600)
        driver.implicitly_wait(180)
        driver.get(url)
        driver.delete_all_cookies()
        for cookie in self.cookies:
            try:
                driver.add_cookie(cookie)
                # driver.add_cookie({'name': cookie['name'], 'value': cookie['value']})
            except:
                pass
        driver.get(url)
        confirmBtm = driver.find_element_by_id('confirm_order')
        print(confirmBtm.text)
        confirmBtm.click()
        while True:
            time.sleep(0.5)
            orderBtn = driver.find_element_by_xpath('//*[@class="order4"]/a')
            if u'确认预约' == orderBtn.text:
                print(u'[{}][{}] 点击确认预约'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), name.replace('\n', ' ')))
                orderBtn.click()

        time.sleep(300)
        driver.quit()

if __name__ == '__main__':
    LeyueRegistration().start()