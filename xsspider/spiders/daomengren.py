#coding=utf-8
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from urlparse import urljoin
from xsspider.items import XsspiderItem, XsdetailItem


class DaomengrenSpider(Spider):
    name = "daomengren"
    allowed_domains = ["www.daomengren.com"]
    start_urls = (
        'http://www.daomengren.com/lastupdate_303/',
        )

    def parse(self, response):
        sel = Selector(response)
        urls = sel.xpath('//a/@href')
        for url in urls.re('^/\d+_\d+/'):
            yield Request(url= urljoin(response.url, url), callback=self.parse_list)
        for url in urls.re('/lastupdate_\d+/'):
            yield Request(url= urljoin(response.url, url), callback=self.parse)
            
    def parse_list(self,response):
        sel = Selector(response)
        item = XsspiderItem()
        item['title'] = sel.xpath('//*[@id="info"]/h1/text()').extract()[0]
        item['category'] = sel.xpath('//*[@id="info"]/p[3]/text()').re(u'：(.*)')[0]
        item['descript'] = ''.join([x.extract() for x in  sel.xpath('//*[@id="intro"]/p[2]/text()')])
        yield item
        
        for url in sel.xpath('//*[@id="list"]/dl/dd/a/@href').extract():
            yield Request(url= urljoin(response.url, url), callback=self.parse_content, meta={'title':item['title']})
        
        
    def parse_content(self, response):
        sel = Selector(response)
        item = XsdetailItem()
        item['content'] = ''.join([x.extract() for x in sel.xpath('//*[@id="content"]/p/text()')]).replace(u'    百度搜索 本书名 + 盗梦人 看最快更新','')
        item['title'] = sel.xpath('//*[@id="box_con"]/div[2]/h1/text()').extract()[0]
        item['xs'] = response.meta['title']
        return item
        
        
         
