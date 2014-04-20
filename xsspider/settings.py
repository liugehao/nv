#coding=utf-8

BOT_NAME = 'xsspider'

SPIDER_MODULES = ['xsspider.spiders']
NEWSPIDER_MODULE = 'xsspider.spiders'
ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline':100,}  
#ITEM_PIPELINES = {'xsspider.images.MyImagesPipeline':100,}  
#'xsspider.pipelines.XsspiderPipeline':200

DATABASE = {'drivername': 'postgresql',
            'host':'127.0.0.1',
            'username': 'postgres',
            'password': 'liuyou',
            'database': 'novel'}
REDIS = {'host':'127.0.0.1', 
            'port':6379, 
            #'db':1
            }
IMAGES_STORE = '/home/l/files'
IMAGES_EXPIRES = 1
IMAGES_THUMBS = {
#    'small':(50, 50),
#    'big': (270, 270)
}
IMAGES_MIN_HEIGHT = 1
IMAGES_MIN_WIDTH = 1

DUPEFILTER_CLASS = 'xsspider.dupefilter.XsDupeFilter'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xsspider (+http://www.yourdomain.com)'

#SCHEDULER = 'scrapy.core.scheduler.Scheduler'
#SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleLifoDiskQueue'
#SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.LifoMemoryQueue'
#SCHEDULER_PERSIST = True
#DOWNLOAD_DELAY = 0
#DOWNLOAD_TIMEOUT = 7200
#CONCURRENT_REQUESTS = 20
JOBDIR = '/home/l/xsspider/job' #坑啊，官方手册中没有这个

