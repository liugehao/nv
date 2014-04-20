#coding=utf-8
from scrapy.dupefilter import BaseDupeFilter
import redis
from scrapy.utils.request import request_fingerprint

from scrapy import log
import urlparse
import time
from datetime import datetime
from scrapy.utils.job import job_dir

class XsDupeFilter(BaseDupeFilter):
    def __init__(self,REDIS):
        self.redis = redis.Redis(**REDIS)
        self.logdupes = True
        
    @classmethod
    def from_settings(cls, settings):
        return cls(settings['REDIS'])
        
    """
    如果　request.meta['expire'] 值存在:　则判断是否过期，过期时间为expire秒，否则返回True不能采集
    如果不存在：redis中有值返回True,否则添加进去重列表
    """
    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        domainname = urlparse.urlsplit(request.url).netloc
        
        redis_value = self.redis.hget(domainname, fp)
        curtime = time.mktime(datetime.now().utctimetuple())
        
        if not request.meta.has_key('expire'):
            if redis_value == True:
                return True
            else:
                self.redis.hset(domainname, fp, True)
        else:            
            if redis_value is None or curtime - float(redis_value) > request.meta['expire']:
                self.redis.hset(domainname, fp, curtime)
            else:
                return True

            
    def request_fingerprint(self, request):
        return request_fingerprint(request)
        
    def log(self, request, spider):
        if self.logdupes:
            fmt = "Filtered duplicate request: %(request)s - no more duplicates will be shown (see DUPEFILTER_CLASS)"
            log.msg(format=fmt, request=request, level=log.DEBUG, spider=spider)
            self.logdupes = False
