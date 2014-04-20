#coding=utf-8


from sqlalchemy.orm import sessionmaker
from models import Novel, NovelDetail, db_connect, create_novel_table
import redis
import settings


class XsspiderPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_novel_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.redis = redis.Redis(**settings.REDIS)

    def process_item(self, item, spider):
        session = self.Session()
        if item.has_key('sort'):
            novel_name = item['novel']
            novel = self.redis.hmget(novel_name,('id','last_detail_id', 'last_detail_title'))
            item['novel'] = novel[0] and novel[0] or 0
            if item['title'].endswith(u"Ｔ") or len(item['images'])>0:
                item['content'] = ','.join(item['images'])
            novel_detail = NovelDetail(novel=item['novel'], title=item['title'], content=item['content'], sort=item['sort'] )
            session.add(novel_detail)
            session.commit()
            
            if novel[1] or novel[1] < item['sort']:
                self.redis.hmset(novel_name, {'last_detail_id':item['sort'], 'last_detail_title':item['title']})            
            return item
        
        if item.has_key('author'):
            novel = Novel(**item)
            session.add(novel)
            session.commit()
            self.redis.hset(novel.name, 'id', novel.id)
        return item

