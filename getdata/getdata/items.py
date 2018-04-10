# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    #公司名称
    com_name = scrapy.Field()
    #公司地址
    com_addr = scrapy.Field()
    #所属区域
    com_area = scrapy.Field()
    #公司类型
    com_class = scrapy.Field()
    #所属行业
    com_trade = scrapy.Field()
    #公司规模
    com_size = scrapy.Field()
    #职位名称
    job_name = scrapy.Field()
    #工作经验
    job_exp = scrapy.Field()
    #教育程度
    job_edu = scrapy.Field()
    #职能类别
    job_class = scrapy.Field()
    #工作关键字
    job_keyword = scrapy.Field()
    #薪资待遇
    job_pay = scrapy.Field()
    #职位信息
    job_info = scrapy.Field()
    #发布日期
    postdate = scrapy.Field()
