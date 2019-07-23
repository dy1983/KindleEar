#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base import BaseFeedBook, URLOpener, string_of_tag
from lib.urlopener import URLOpener # 导入请求URL获取页面内容的模块
from bs4 import BeautifulSoup # 导入BeautifulSoup处理模块

def getBook():
    return NYTChinese

class NYTChinese(BaseFeedBook):
    title                 = u'纽约时报中文网'
    description           = u'纽约时报中文网 国际纵览'
    language              = 'zh-cn'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_nytchinese.gif"
    coverfile             = "cv_nytchinese.jpg"
    oldest_article        = 7
    
    feeds = [
        (u'国际纵览', 'https://cn.nytimes.com/rss/'),
    ]
    
    # fulltext_by_readability = False
    
    keep_only_tags = [
        dict(name='div', class_='article-header'),
        dict(name='div', class_='article-paragraph'),
    ]
    
    max_articles_per_feed = 20 # 设定每个主题下要最多可抓取的文章数量
