# -*- coding: utf-8 -*-
import re
import time

import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import logging

from TmallShoes import settings
from TmallShoes.items import TmallshoesItem


class TmallshoesSpider(scrapy.Spider):
    name = 'tmallshoes'

    def __init__(self):
        super(TmallshoesSpider, self).__init__()
        self.start_urls = ['https://login.tmall.com']
        self.header = {
            ':authority': 'www.tmall.com',
            ':method': 'GET',
            ':path': '/',
            ':scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,la;q=0.8,zh-CN;q=0.7,zh;q=0.6',
            'cookie': 'cna=ePLLErrWDmMCAd7Rn9geKLC0; sm4=510100; enc=Dsie48beNZnGMeD0gQ%2FrASzQokgpuU08ZeDJMiPGBrqjo7d4ylpjRzlK0tbYZYiscj01hFASqe0Trn826pI2pQ%3D%3D; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; hng=""; _m_h5_tk=3983183c8abfe7539b6ce1f2aa05ce07_1537891564152; _m_h5_tk_enc=f2318580318581393469030513baa9fa; cookie2=16ec11ec198f9fa0530279da39017633; t=bab650ad34d2258af7a1a5a73cf67e47; _tb_token_=ebbe5ee75e8e3; cq=ccp%3D1; isg=BPz8Cmp9iyWCur_NwQpoNrKVzZpuXb_LSCiKBNZ9FOfKoZwr_gEOrmEThYF80th3; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=UtASsssmfaCONGki4KTH3w%3D%3D&cookie15=VT5L2FSpMGV7TQ%3D%3D&existShop=false&pas=0&cookie14=UoTfLJ1SD9BdPQ%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByRuSbkkERgkBYG8%3D&id2=UNX6wDxbEN0L&nk2=G5eKtUAq%2Fig%3D&lg2=W5iHLLyFOGW7aA%3D%3D; tracknick=xwzjying; _l_g_=Ug%3D%3D; ck1=""; unb=351217137; lgc=xwzjying; cookie1=AiazX8pkl9KOKD%2B69Bi96Yl6pyc8UHFmM%2F6gE5ckkno%3D; login=true; cookie17=UNX6wDxbEN0L; _nk_=xwzjying; uss=""; csg=030a8f14; skt=7f760a268598bd25',
            'if-none-match': 'W/"3742a-H6/8Fiog/wU64j915+r1tSE+4Bw"',
            'referer': 'https://login.tmall.com/?spm=875.7931836/B.a2226mz.1.66144265wFwUvf&redirectURL=https%3A%2F%2Fwww.tmall.com%2F',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3521.2 Safari/537.36'
        }
        # self.allowed_domain = ['www.tmall.com']
        '''
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('--disable-gpu')
        option.add_argument(settings.USER_AGENT)
        self.browser = webdriver.Chrome(executable_path=r'C:/ProgramData/Anaconda3/Library/bin/chromedriver.exe',
                                        chrome_options=option)
        # self.browser.set_page_load_timeout(10)
        '''
        self.browser = webdriver.Chrome(executable_path=r'C:/ProgramData/Anaconda3/Library/bin/chromedriver.exe')
        self.wait = WebDriverWait(self.browser, 20000)

    def parse(self, response):
        url_set = set()
        self.browser.get(response.url)
        time.sleep(5)
        # 模拟登陆

        login_frame = self.wait.until(
            lambda browser: browser.find_element_by_id('J_loginIframe')
        )

        self.browser.switch_to_frame('J_loginIframe')

        to_login = self.wait.until(
            lambda browser: browser.find_element_by_id('J_Quick2Static')
        )
        to_login.click()

        username = self.wait.until(
            lambda browser: browser.find_element_by_id('TPL_username_1')
        )
        username.clear()
        username.send_keys('xwzjying')

        password = self.wait.until(
            lambda browser: browser.find_element_by_id('TPL_password_1')
        )
        password.clear()
        password.send_keys('201310Xiongwei')
        time.sleep(20)
        login = self.wait.until(
            lambda browser: browser.find_element_by_id('J_SubmitStatic')
        )
        login.click()
        # 输入查询和排序条件，加载第一页内容
        input = self.wait.until(
            lambda browser: browser.find_element_by_xpath('//*[@id="mq"]')
        )
        input.send_keys('女鞋')
        submit = self.wait.until(
            lambda browser: browser.find_element_by_xpath('//*[@id="mallSearch"]/form/fieldset/div/button')
        )
        submit.click()
        input_price = self.wait.until(
            lambda browser: browser.find_element_by_xpath('//*[@id="J_FPrice"]/div[1]/b[1]/input')
        )
        input_price.clear()
        input_price.send_keys('2000')
        submit_price = self.wait.until(
            lambda browser: browser.find_element_by_xpath('//*[@id="J_FPEnter"]')
        )
        submit_price.click()

        sort = self.wait.until(
            lambda browser: browser.find_element_by_xpath('//*[@id="J_Filter"]/a[4]')
        )
        sort.click()
        url = self.browser.current_url
        print('++++++++++++++++++++++++++++++++++++++++++++++++++' + url)
        url_set.add(url)
        # 点击下一页或者输入页面跳转到指定页面，获取页面URL
        for i in range(2, 10):
            next_input = self.wait.until(
                lambda browser: browser.find_element_by_xpath(
                    '//*[@id="content"]/div/div[@class="ui-page"]/div/b[@class="ui-page-skip"]/form/input[@name="jumpto"]')
            )
            next_input.clear()
            next_input.send_keys(i)
            next_submit = self.wait.until(
                lambda browser: browser.find_element_by_xpath(
                    '//*[@id="content"]/div/div[@class="ui-page"]/div/b[@class="ui-page-skip"]/form/button')
            )

            '''
            next_submit = self.wait.until(
                lambda browser: browser.find_element_by_xpath(
                    '//*[@id="content"]/div/div[@class="ui-page"]/div/b[@class="ui-page-num"]/a[@class="ui-page-next"]')
            )
            '''
            next_submit.click()
            time.sleep(5)
            url = self.browser.current_url
            url_set.add(url)
            print('-------------------------------------------------------------' + url)
        for url in url_set:
            yield scrapy.Request(url, callback=self.parse_content)

    def parse_content(self, response):
        sites = response.xpath('//*[@id="J_ItemList"]/div[@class="product  "]/div[@class="product-iWrap"]')
        products = []
        for site in sites:
            product = TmallshoesItem()
            title = site.xpath(
                './p[@class="productTitle"]/a/@title').extract()
            # product['title'] = [t for t in title]
            for t in title:
                product['title'] = t
            link = site.xpath(
                './div[@class="productImg-wrap"]/a/@href').extract()
            # product['link'] = [l for l in link]
            for l in link:
                product['link'] = 'https:' + l
            price = site.xpath(
                './p[@class="productPrice"]/em/text()').extract()
            # product['price'] = [p for p in price]
            for p in price:
                product['price'] = p
            deal = site.xpath(
                './p[@class="productStatus"]/span/em/text()').extract()
            # product['deal'] = [d for d in deal]
            for d in deal:
                product['deal'] = d[:-1]
            shop = site.xpath(
                './div[@class="productShop"]/a/text()').extract()
            # product['shop'] = [p for p in shop]
            for s in shop:
                product['shop'] = s.replace('\n', '')
            products.append(product)
        yield products
