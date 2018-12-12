#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/12/12
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pyquery import PyQuery as pq
import time
import xlwt

browser = webdriver.Chrome(executable_path=r'D:\crawler_tools\chromedriver_win32\chromedriver.exe')
wait = WebDriverWait(browser, 10)

All = []
count = 0


# 获取输入框
def login_search(key):
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#content>div.linputer>div.rinput>input.inputer')))
    input.send_keys(key)
    input.send_keys(Keys.ENTER)


# 爬取页面
def parse_html(html):
    global count
    doc = pq(html)
    items = doc(".list .activeable").items()  # 生成器
    for item in items:
        str = item.attr('data-positionid')
        if not str:
            break
        product = {
            'url': "http://m.lagou.com/jobs/" + item.attr('data-positionid') + ".html",
            'company': item.find('.item-title').text(),
            'position': item.find('.item-pos').text(),
            'salary': item.find('.item-salary').text(),
            'publish_time': item.find('.item-time').text()
        }
        if len(set(product.values())) > 1:
            All.append(product)


# 分页
def get_more_page():

    global count

    html = ''
    try:
        more = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#content > div.listcon > ul.list > li.list-more")))
        print(more.text)
        for i in range(900):
            time.sleep(1)
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)", "")
            more.click()
            count += 1
        html = browser.page_source
        print('load page:{}'.format(str(count)))
    except Exception as e:
        print('Error:{}'.format(e))
        parse_html(html)
        return None
    else:
        parse_html(html)


if __name__ == '__main__':
    url = 'http://m.lagou.com/search.html'
    browser.get(url)
    login_search('python')
    get_more_page()
    print(All)


    filename = 'python.xlsx'

    wbook = xlwt.Workbook()
    wsheet = wbook.add_sheet('python')
    style = xlwt.easyxf('align:vertical center, horizontal center')
    wsheet.write(0, 0, u'公司', style)
    # wsheet.write(0, 1, u'职位类别', style)
    wsheet.write(0, 1, u'位置', style)
    wsheet.write(0, 2, u'薪资', style)
    wsheet.write(0, 3, u'发布时间', style)
    wsheet.write(0, 4, u'链接', style)

    row = 1
    col = 0
    for i in All:
        company = i['company']
        position = i['position'].replace(" ", '')
        salary = i['salary']
        publish_time = i['publish_time']
        url = i['url']
        wsheet.write(row, col, company)
        # wsheet.write(row, col + 1, category)
        wsheet.write(row, col + 1, position)
        wsheet.write(row, col + 2, salary)
        wsheet.write(row, col + 3, publish_time)
        wsheet.write(row, col + 4, url)
        row += 1
    wbook.save(filename)