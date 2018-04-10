import scrapy
import re
import time
from ..items import JobsItem

class GetjobSpider(scrapy.Spider):
    name = 'getjob'
    fname = 'data'
    allowed_domains = ['51job.com']
    base_url = 'https://search.51job.com/list/090200,000000,0000,00,9,99,' \
               '%25E6%259C%25BA%25E5%2599%25A8%25E5%25AD%25A6%25E4%25B9%25A0%2Bor' \
               '%2B%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%2Bor' \
               '%2B%25E7%25AE%2597%25E6%25B3%2595%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,' \
               '2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&' \
               'jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&' \
               'fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    start_urls = []

    page = 1
    maxpage = 1

    def __init__(self):
        self.start_urls.append(self.base_url.format(self.page))
        self.fname = 'data/data_{}.csv'.format(time.strftime('%Y%m%d_%H%M%S', time.localtime()))

    def parse(self, response):
        #获取总页数
        if self.page == 1:
            strpage = response.css('.dw_page>.p_box>.p_wp>.p_in>span::text').extract_first()
            self.maxpage = int(re.search(r'\d+', strpage).group(0))
        print('第{}页/共{}页'.format(self.page, self.maxpage))
        #获取详情页连接列表
        strList = response.css('#resultList>.el')
        for strItem in strList:
            strUrl = strItem.css('.t1>span>a::attr(href)').extract_first()
            if strUrl is not None:
                yield scrapy.Request(strUrl, callback=self.parseInfo)
        self.page += 1
        if self.page <= self.maxpage:
            yield scrapy.Request(self.base_url.format(self.page), callback=self.parse)

    def parseInfo(self, response):
        info = response.css('.tCompanyPage>.tCompany_center')
        job_name = info.css('.tHeader>.in>.cn>h1::attr(title)').extract_first()
        com_area = info.css('.tHeader>.in>.cn>.lname::text').extract_first()
        com_name = info.css('.tHeader>.in>.cn>.cname>a::attr(title)').extract_first()
        ltype = info.css('.tHeader>.in>.cn>.ltype::text').extract_first()
        com_class = None
        com_size = None
        com_trade = None
        if ltype is not None:
            ntype = ltype.replace('&nbsp;', '').split('|')
            if len(ntype) == 3:
                com_class = ntype[0].strip()
                com_size = ntype[1].strip()
                com_trade = ntype[2].strip()
        job_pay = info.css('.tHeader>.in>.cn>strong::text').extract_first()
        inbox = info.css('.tCompany_main>.tBorderTop_box>.inbox>.t1>.sp4::text').extract()
        job_exp = None
        job_edu = None
        postdate = None
        if len(inbox) == 4:
            job_exp = inbox[0].strip('" ')
            job_edu = inbox[1].strip('" ')
            postdate = inbox[3].strip('" ')
        jobinfo = info.css('.tCompany_main>.tBorderTop_box>.job_msg>p::text').extract()
        job_info = '|'.join(jobinfo)
        jobmsg = info.css('.tCompany_main>.tBorderTop_box>.job_msg>.mt10>.fp>.el::text').extract()
        job_class = jobmsg[0]
        job_keyword = None
        if len(jobmsg)>1:
            job_keyword = '|'.join(jobmsg[1:])
        com_addr = info.css('.tCompany_main>.tBorderTop_box>.bmsg>.fp::text').extract()
        item = JobsItem()
        item['com_name'] = com_name
        if com_addr is not None:
            item['com_addr'] = com_addr[-1].strip('" \t')
        item['com_area'] = com_area
        item['com_class'] = com_class
        item['com_trade'] = com_trade
        item['com_size'] = com_size
        item['job_name'] = job_name
        item['job_exp'] = job_exp
        item['job_edu'] = job_edu
        item['job_class'] = job_class
        item['job_keyword'] = job_keyword
        item['job_pay'] = job_pay
        item['job_info'] = job_info
        item['postdate'] = postdate
        return item



