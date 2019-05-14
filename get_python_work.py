# ！/usr/bin/env python
# -*- coding:utf-8 -*-

import random

from multiprocessing.dummy import Pool  # 多线程，以相同api实现的

import requests
from lxml import etree
import xlwt

from parse_boss.settings import USER_AGENT_LIST


def get_page(url):
    proxy_url = "http://127.0.0.1:3289/pop"
    proxy = requests.get(url=proxy_url).json()
    print(proxy)
    ua = {'User-Agent': random.choice(USER_AGENT_LIST)}
    html = requests.get(url=url, headers=ua, proxies=proxy).text
    # print(html)
    with open('1.html', 'w', encoding='utf-8') as fp:
        fp.write(html)
    return html


def get_detail(html):
    tree = etree.HTML(html)
    # 职位名称
    # work_title = tree.xpath('//div[@class="info-primary"]/div[2]/h1/text()')[0]
    # print(work_title)
    # 获取职位要求信息
    # description_of_job = tree.xpath('//[@class="job-detail"]/div[2]/div[1]/div/text()')
    description_of_job = tree.xpath('//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div//text()')
    print(description_of_job)
    # return {'title': work_title, 'description': "".join(description_of_job)}
    # return { 'description': "".join(description_of_job)}
    return "".join(description_of_job)


def parse_page(html):
    """
    解耦，一页一页的一个一个li解析
    :param html:
    :return: 生成器返回页面中每一个li标签的定向内容
    """
    tree = etree.HTML(html)
    # 所有的li
    li_ele = tree.xpath('//div[@class="job-list"]/ul/li')
    for li in li_ele:
        detail_url = li.xpath('./div/div[1]/h3/a/@href')[0]
        detail_url = f'https://www.zhipin.com{detail_url}'
        # 请求获取工作详情
        detail_html = get_page(detail_url)
        detail_data = get_detail(detail_html)

        title = li.xpath('./div/div[1]/h3/a/div[1]/text()')[0]
        salary = li.xpath('./div/div[1]/h3/a/span[1]/text()')[0]
        # 公司信息
        company = li.xpath('./div/div[2]//h3/a/text()')[0]
        company_info = li.xpath('./div/div[2]//p/text()')
        company_category = company_info[0]
        if len(company_info) < 3:
            company_has_line = None
            company_count = company_info[1]
        else:
            company_has_line = company_info[1]
            company_count = company_info[2]

        yield {
            'company': company,
            'company_category': company_category,
            'company_has_line': company_has_line,
            'company_count': company_count,
            'title': title,
            'salary': salary,
            'detail_url': detail_url,
            'detail_data': detail_data,
        }


def save_data(page):
    global worksheet, row, col, style
    for data in page:
        worksheet.write(row, col, data["company"], style)
        worksheet.write(row, col + 1, data["company_category"], style)
        worksheet.write(row, col + 2, data["company_has_line"], style)
        worksheet.write(row, col + 3, data["company_count"], style)
        worksheet.write(row, col + 4, data["title"], style)
        worksheet.write(row, col + 5, data["salary"], style)
        worksheet.write(row, col + 6, data["detail_url"], style)
        worksheet.write(row, col + 7, data["detail_data"], style)
        row += 1


def main():
    import time
    start = time.time()
    pool = Pool(10)

    base_url = "https://www.zhipin.com/c101010100/?query=python&page={0}&ka=page-{0}"
    page_urls = [base_url.format(i) for i in range(1, 11)]

    html_page_list = pool.map(get_page, page_urls)  # 开多线程请求10个页面，返回为一个生成器

    parse_data_list = pool.map(parse_page, html_page_list)  # 开多线进行解析

    pool.map(save_data, parse_data_list)

    workbook.save('boss_python_bj.xls')
    # for page in parse_data_list:
    #     print("page:", page)
    #     for data in page:
    #         worksheet.write(row, col, data["company"], style)
    #         worksheet.write(row, col + 1, data["company_category"], style)
    #         worksheet.write(row, col + 2, data["company_has_line"], style)
    #         worksheet.write(row, col + 3, data["company_count"], style)
    #         worksheet.write(row, col + 4, data["title"], style)
    #         worksheet.write(row, col + 5, data["salary"], style)
    #         worksheet.write(row, col + 6, data["detail_url"], style)
    #         row += 1

    # workbook.save('xxxxpython.xls')
    pool.close()
    pool.join()

    print('total_time:', time.time() - start)  # total_time: 1.162891149520874


if __name__ == '__main__':
    # 先创建工作薄及预设好样式及标题列
    # 编辑格式
    style = xlwt.easyxf('align:vertical center, horizontal center')
    workbook = xlwt.Workbook(encoding='utf-8')
    # 在工作薄里创建一个标签
    worksheet = workbook.add_sheet('boss')
    row = 1
    col = 0
    # 写入标题行
    worksheet.write(0, 0, '公司名称', style)
    worksheet.write(0, 1, '公司类别', style)
    worksheet.write(0, 2, '融资情况', style)
    worksheet.write(0, 3, '公司规模', style)
    worksheet.write(0, 4, '招聘岗位', style)
    worksheet.write(0, 5, '薪资', style)
    worksheet.write(0, 6, '工作内容', style)
    worksheet.write(0, 7, '职位要求', style)
    # 运行主函数
    main()

"""
请求使用异步io
解析时使用多线程或多进程
"""


# 第一版同步爬取一页
# def get_urls(link):
#     """
#     获取所有的python开发的url
#     :param link:
#     :return:
#     """
#     proxy = {'http': '1.197.203.33'}
#     ua = {'User-Agent': random.choice(USER_AGENT_LIST)}
#     html = requests.get(url=link, headers=ua, proxies=proxy).text
#     tree = etree.HTML(html)
#
#     style = xlwt.easyxf('align:vertical center, horizontal center')
#     workbook = xlwt.Workbook(encoding='utf-8')
#     # 在工作薄里创建一个标签
#     worksheet = workbook.add_sheet('boss')
#     # 写入标题行
#     worksheet.write(0, 0, '公司名称', style)
#     worksheet.write(0, 1, '公司类别', style)
#     worksheet.write(0, 2, '融资情况', style)
#     worksheet.write(0, 3, '公司规模', style)
#     worksheet.write(0, 4, '招聘岗位', style)
#     worksheet.write(0, 5, '薪资', style)
#     worksheet.write(0, 6, '工作内容', style)
#     worksheet.write(0, 7, '职位要求', style)
#
#     row = 1
#     col = 0
#     # 所有的li
#     li_ele = tree.xpath('//div[@class="job-list"]/ul/li')
#
#     url_list = []
#     for li in li_ele:
#         print(li)
#         url = li.xpath('./div/div[1]/h3/a/@href')[0]
#         url = f'https://www.zhipin.com{url}'
#         url_list.append(url)
#         print(url)
#         title = li.xpath('./div/div[1]/h3/a/div[1]/text()')[0]
#         print(title)
#         salary = li.xpath('./div/div[1]/h3/a/span[1]/text()')[0]
#         print(salary)
#         # 公司信息
#         company = li.xpath('./div/div[2]//h3/a/text()')[0]
#         print(company)
#         company_info = li.xpath('./div/div[2]//p/text()')
#         company_category = company_info[0]
#         print(company_category)
#         if len(company_info) < 3:
#             company_has_line = None
#             company_count = company_info[1]
#         else:
#             company_has_line = company_info[1]
#             company_count = company_info[2]
#
#         print(company_category)
#         print(company_has_line)
#         print(company_count)
#         # 保存到excel
#         worksheet.write(row, col, company, style)
#         worksheet.write(row, col + 1, company_category, style)
#         worksheet.write(row, col + 2, company_has_line, style)
#         worksheet.write(row, col + 3, company_count, style)
#         worksheet.write(row, col + 4, title, style)
#         worksheet.write(row, col + 5, salary, style)
#         row += 1
#     workbook.save('python_boss.xlsx')
#     return url_list
#
#
# def save_detail(parse_data):
#     global work_want_dict, fb
#     for data in parse_data:
#         print("ccccccc", data)
#         detail_link = data["detail_url"]
#         html = get_page(detail_link)
#         print("ddddd:", html)
#         detail_data = get_detail(html)
#
#         # 构建职位对应要求的大字典
#
#         work_title = detail_data["title"]
#         description_of_job = detail_data["description"]
#         if work_title not in work_want_dict:
#             work_want_dict[work_title] = [description_of_job]
#         else:
#             work_want_dict[work_title].append(description_of_job)
#
#         import json
#         fb.write(json.dumps(work_want_dict))
#
#
# def detail_main():
#     import time
#     start = time.time()
#     pool = Pool(10)
#
#     base_url = "https://www.zhipin.com/c101010100/?query=python&page={0}&ka=page-{0}"
#     page_urls = [base_url.format(i) for i in range(1, 11)]
#     print(page_urls)
#
#     html_page_list = pool.map(get_page, page_urls)  # 开多个线程一下子将10个页面获取到，返回为一个生成器
#
#     parse_data_list = pool.map(parse_page, html_page_list)  # 拿到每个页面多线程进行解析
#
#     pool.map(save_detail, parse_data_list)
#
#     pool.close()
#     pool.join()
#     print('total_time:', time.time() - start)  # total_time: 1.162891149520874

# fb = open('python_info.json', 'a', encoding='utf-8')
# work_want_dict = {}
# detail_main()
# fb.close()
