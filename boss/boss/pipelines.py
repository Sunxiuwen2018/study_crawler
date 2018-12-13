# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BossPipeline(object):
    fp = None

    def open_spider(self, spider):
        self.fp = open('./qiubai.csv', 'w', encoding='utf-8')
        print("开始爬虫")

    def process_item(self, item, spider):
        # 取出item对象

        job_title = item['job_title']
        salary = item['salary']
        url = item['url']
        company = item['company']
        release_time = item['release_time']

        self.fp.write(company + "@" + job_title + "@" + salary + "@" + release_time + "@" + url + "\n")
        return item

    def close_spider(self, spider):
        self.fp.close()
        print("结束爬虫")
