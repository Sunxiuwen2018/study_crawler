#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/12/17
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
    'Connection': 'close'
}


# asyncio
def parse_content(url):
    """获取小说详情页的内容
    返回章节和内容
    """
    res = requests.get(url=url, headers=headers)
    res.encoding = 'gb18030'
    res = res.text
    soup = BeautifulSoup(res, 'lxml')
    title = soup.select('#chapter_title > h1')[0].get_text()
    next_url = soup.select('.chapter_pager .nextLink')[0]['href']
    next_url = 'https://www.23zw.me/olread/65/65768/' + next_url
    page_content = soup.find('div', id="text_area").text
    page_content = page_content.replace(' ' * 4, '\n')
    return title, page_content, next_url


if __name__ == '__main__':
    f = open('./sx.txt', 'w', encoding='utf-8')
    next_url = 'https://www.23zw.me/olread/65/65768/f1cde65eec245df86dd07ed86b921ab2.html'
    while next_url:
        title, content, next_url = parse_content(next_url)
        f.write(title + '\n' + content)

        next_url = next_url
