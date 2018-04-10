# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv

class JobsPipeline(object):
    def process_item(self, item, spider):
        fname = spider.fname
        di = dict(item)
        heard = list(di.keys())
        if not os.path.exists(fname):
            with open(fname, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=heard)
                writer.writeheader()
        with open(fname, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=heard)
                writer.writerow(di)
        return item
