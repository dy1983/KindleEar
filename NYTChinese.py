#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base import BaseFeedBook

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
    oldest_article        = 1
    
    feeds = [
            (u'国际纵览', 'https://cn.nytimes.com/rss/'),
            ]
    
    def fetcharticle(self, url, opener, decoder):
        #每个URL都增加一个后缀full=y，如果有分页则自动获取全部分页
        url += '?full=y'
        return BaseFeedBook.fetcharticle(self,url,opener,decoder)
        