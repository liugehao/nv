# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

def str2int(i):
    try:
        return int(i)
    except:
        return 0

class XsspiderItem(Item):
    name = Field()
    category = Field()
    author = Field()
    status = Field()
    hits = Field()
    hits_month = Field()
    hits_week = Field()
    recommend = Field()
    recommend_month = Field()
    recommend_week = Field()
    favorites = Field()
    descript = Field()
    
    
class XsdetailItem(Item):
    novel = Field()
    title = Field()
    content = Field()
    sort = Field()
    image_urls = Field()
    images = Field()
    
