# -*- coding: utf-8 -*-
import re

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
    allowed_domains = ['www.tmall.com']
    start_urls = ['https://www.tmall.com']

    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('--disable-gpu')
        option.add_argument(settings.USER_AGENT)
        self.browser = webdriver.Chrome(executable_path=r'C:/ProgramData/Anaconda3/Library/bin/chromedriver.exe',
                                        chrome_options=option)
        self.browser.set_window_size(1440, 900)
        self.wait = WebDriverWait(self.browser, 10)
        super(TmallshoesSpider, self).__init__()
        dispatcher.connect(self.spider_closed,
                           signals.spider_closed)  # 第二个参数是信号（spider_closed:爬虫关闭信号，信号量有很多）,第一个参数是当执行第二个参数信号时候要执行的方法

    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭chrome
        print('spider closed')
        self.browser.quit()

    def parse(self, response):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        total = response.xpath('//*[@id="content"]/div/div[9]/div/b[2]/form/text()').extract()
        total = ''.join(total).replace('\n', '').replace(' ', '')
        total = int(re.compile('(\d+)').search(total).group(1))
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
        return products
