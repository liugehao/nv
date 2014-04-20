#coding=utf-8
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from urlparse import urljoin
from xsspider.items import XsspiderItem, XsdetailItem


class AbcseeSpider(Spider):
    name = "abcsee"
    allowed_domains = ["abcsee.net"]
#    start_urls = (
#    'http://www.abcsee.net/book/0/320/'
#        'http://www.abcsee.net/class/1-95.html',

#        'http://www.abcsee.net/class/2-35.html',
#        'http://www.abcsee.net/class/3-245.html',
#        'http://www.abcsee.net/class/4-295.html',
#        'http://www.abcsee.net/class/6-26.html',
#        'http://www.abcsee.net/class/7-63.html',
#        'http://www.abcsee.net/class/10-44.html',

#        )
    def start_requests(self):
        return [Request("http://www.abcsee.net/book/0/320/161550.html",meta=dict(sort=1,name='a'),
                            callback=self.parse_detail)]
    def parse(self, response):
        sel = Selector(response)
        for node in sel.xpath('//*[@id="content"]/dd[1]/table/tr/td[1]/a'):
            url = node.xpath('@href').extract()[0]
            yield Request(url=url, callback=self.parse_descript, meta={'name':node.xpath('text()').extract()[0]})
            
    def parse_descript(self, response):
        sel = Selector(response)
        item = XsspiderItem()
        item['name'] = response.meta['name']
        item['category'] = sel.xpath('//*[@id="at"]/tr[1]/td[1]/a/@href').re('class=(\d+)$')[0]
        item['author'] = sel.xpath('//*[@id="at"]/tr[1]/td[2]/text()').extract()[0].strip()
        item['status'] = sel.xpath('//*[@id="at"]/tr[1]/td[3]/text()').extract()[0].strip()
        item['hits'] = sel.xpath('//*[@id="at"]/tr[3]/td[1]/text()').extract()[0].strip()
        item['hits_month'] = sel.xpath('//*[@id="at"]/tr[3]/td[2]/text()').extract()[0].strip()
        item['hits_week'] = sel.xpath('//*[@id="at"]/tr[3]/td[3]/text()').extract()[0].strip()
        item['recommend'] = sel.xpath('//*[@id="at"]/tr[4]/td[1]/text()').extract()[0].strip()
        item['recommend_month'] = sel.xpath('//*[@id="at"]/tr[4]/td[2]/text()').extract()[0].strip()
        item['recommend_week'] = sel.xpath('//*[@id="at"]/tr[4]/td[3]/text()').extract()[0].strip()
        item['favorites'] = sel.xpath('//*[@id="at"]/tr[2]/td[1]/text()').extract()[0].strip()
        item['descript'] = sel.xpath('//*/dd/p[2]/text()').extract()[0]
        yield item
        yield Request(url=urljoin(response.url, sel.xpath('//*[@class="read"]/@href').extract()[0]), callback=self.parse_list, meta={'name':item['name'], 'expire':3600 * 24})
        
    def parse_list(self, response):
        sel = Selector(response)
        i = 0
        for url in sel.xpath('//*[@id="at"]/tr/td/a/@href').extract():
            i += 1
            yield Request(url=urljoin(response.url, url), callback=self.parse_detail, meta={'sort':i,'name':response.meta['name']})
        
        
    def parse_detail(self, response):
        sel = Selector(response)
        item = XsdetailItem()
        item['title'] = sel.xpath('//*[@id="amain"]/dl/dd[1]/h1/text()').extract()[0].strip()
        item['sort'] = response.meta['sort']
        item['novel'] = response.meta['name']
        if item['title'].strip().endswith(u"Ｔ"):
            item['image_urls'] = sel.xpath('//*[@id="contents"]/div[3]/img/@src').extract()
        else:
            item['content'] = ''.join([x for x in sel.xpath('//*[@id="contents"]/text()').extract()])
        print item['title'], item
        return item
