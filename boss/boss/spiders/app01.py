# -*- coding: utf-8 -*-
import scrapy
from boss.items import BossItem


class App01Spider(scrapy.Spider):
    name = 'app01'
    # allowed_domains = ['https://www.zhipin.com/']
    start_urls = ['https://www.zhipin.com/c101210100/?query=python&page=1']
    url = 'https://www.zhipin.com/c101210100/?query=python&page='
    pageNum = 1

    def parse(self, response):
        li_list = response.xpath('//div[@class="job-list"]/ul/li')
        # 用于递归终止条件
        next_href = response.xpath('//div[@class="page"]/a[@ka="page-next"]/@href').extract_first()
        for li in li_list:
            job_title = li.xpath('./div/div[1]/h3/a/div[1]/text()')[0].extract()
            salary = li.xpath('./div/div[1]/h3/a/span/text()')[0].extract()
            url = 'https://www.zhipin.com' + li.xpath('./div/div[1]/h3/a/@href').extract_first()
            company = li.xpath('./div/div[2]/div[1]/h3/a/text()').extract_first()
            release_time = li.xpath('./div/div[3]/p/text()').extract_first()
            item = BossItem()
            item['job_title'] = job_title
            item['salary'] = salary
            item['url'] = url
            item['company'] = company
            item['release_time'] = release_time
            yield item
        if next_href:
            # 如果next标签没有href了就终止
            self.pageNum += 1  # 从第二页开始
            new_url = self.url + str(self.pageNum)
            # 回调函数
            yield scrapy.Request(url=new_url, callback=self.parse)
