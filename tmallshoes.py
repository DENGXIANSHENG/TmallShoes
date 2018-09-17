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
    print("searching")
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
        return total
    except TimeoutException:
        search()


def next_page(page_number):
    print("next page")
    try:
        input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#content > div > div.ui-page > div > b.ui-page-skip > form > input.ui-page-skipTo"))
        )
        input.clear()
        input.send_keys(page_number)
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#content > div > div.ui-page > div > b.ui-page-skip > form > button"))
        )
        submit.click()

        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "#content > div > div.ui-page > div > b.ui-page-num > b.ui-page-cur"),
                str(page_number))
        )
    except TimeoutException:
        next_page(page_number)


def main():
    try:
        page_number = search()
        for i in range(2,page_number+1):
            next_page(i)
    except Exception:
        print("Error")

if __name__ == "__main__":
    main()
