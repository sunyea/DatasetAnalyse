# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class JobsPipeline(object):
    def process_item(self, item, spider):
        fname = spider.fname
        di = dict(item)
        if not os.path.exists(fname):
            with open(fname, 'w', encoding='utf8') as f:
                f.write(':::'.join(list(di.keys())))
                f.write('\n')
        with open(fname, 'a', encoding='utf8') as f:
            f.write(':::'.join(list(di.values())))
            f.write('\n')
        return item
