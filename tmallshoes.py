import pymongo
import json

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pyquery import PyQuery as pq

'''
# selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH. Please see 
https://sites.google.com/a/chromium.org/chromedriver/home
# 下载Chromedriver，然后解压到目录(目录可以自行决定)，然后将目录路径添加到调用参数中去,添加chromedriver路径
'''
browser = webdriver.Chrome(r"/anaconda3/bin/chromedriver")

wait = WebDriverWait(browser, 10)


def search():
    try:
        browser.get("https://www.tmall.com")
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mq"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mallSearch > form > fieldset > div > button"))
        )
        input.send_keys("女鞋")
        submit.click()

        inprice = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_FPrice > div.fP-box > b:nth-child(1) > input"))
        )
        inprice.send_keys("2000")
		
        submitprice = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_FPrice > div.fP-expand > #J_FPEnter"))
        )
        submitprice.click()

        order = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_Filter > a:nth-child(4)"))
        )
        order.click()

        total = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#content > div > div.ui-page > div > b.ui-page-skip > form"))
        )
        total = int(re.compile('(\d+)').search(total.text).group(1))
        print(total)

    except TimeoutException:
        search()


def main():
    search()


if __name__ == "__main__":
    main()
