from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import Sequence
import settings

Base = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))

def create_novel_table(engine):
    Base.metadata.create_all(engine)


    """
        name = Field()
    category = Field()
    author = Field()
    status = Field()
    hits = Field()
    hits_month = Field()
    hits_week = Field()
    recommend = Field()
    recommend_month = Field()
    recomment_week = Field()
    favorites = Field()
    descript = Field()
    """
    
class Novel(Base):
    __tablename__ = "novel"
    id = Column(Integer, Sequence('novel_id_seq'), primary_key=True)
    name = Column('name', String(30))
    category = Column('category', Integer)
    author = Column('author', String(20))
    status = Column('status', String(10))
    hits = Column('hits', Integer)
    hits_month = Column('hits_month', Integer)
    hits_week = Column('hits_week', Integer)
    recommend = Column('recommend', Integer)
    recommend_month = Column('recommend_month', Integer)
    recommend_week = Column('recomment_week', Integer)
    favorites = Column('favorites', Integer)
    descript = Column('descript', Text)
    
    
"""
    name = Field()
    title = Field()
    content = Field()
    sort = Field()
"""
class NovelDetail(Base):
    __tablename__ = "novel_detail"
    id = Column(Integer, Sequence('novel_detail_id_seq'), primary_key=True)
    novel = Column('novel_id', Integer)
    title = Column('title', String(40))
    content = Column('content', Text)
    sort = Column('sort', Integer)
    

if __name__ == "__main__":
    engine = db_connect()
    create_novel_table(engine)
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
