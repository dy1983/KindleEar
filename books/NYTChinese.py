#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base import BaseFeedBook
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
    # oldest_article        = 1
    
    feeds = [
        (u'首页', 'https://cn.nytimes.com/'),
        (u'国际', 'https://cn.nytimes.com/world/'),
        (u'中国', 'https://cn.nytimes.com/china/'),
        (u'经济', 'https://cn.nytimes.com/business/'),
        (u'镜头', 'https://cn.nytimes.com/lens/'),
        (u'科技', 'https://cn.nytimes.com/technology/'),
        (u'科学', 'https://cn.nytimes.com/science/'),
    ]
    
    fulltext_by_readability = False # 设定手动解析网页
    
    keep_only_tags = [
        dict(name='div', class_='article-header'),
        dict(name='div', class_='article-paragraph'),
    ]

    def ParseFeedUrls(self):
        urls = [] # 定义一个空的列表用来存放文章元组
        # 循环处理fees中两个主题页面
        for feed in self.feeds:
            # 分别获取元组中主题的名称和链接
            topic, url = feed[0], feed[1]
            # 请求主题链接并获取相应内容
            opener = URLOpener(self.host, timeout=self.timeout)
            result = opener.open(url)
            # 如果请求成功，并且页面内容不为空
            if result.status_code == 200 and result.content:
                # 将页面内容转换成BeatifulSoup对象
                soup = BeautifulSoup(result.content, 'lxml')
                # 找出当前页面文章列表中所有文章条目
                items = soup.find_all(name='h3', class_='regularSummaryHeadline')
                # 循环处理每个文章条目
                for item in items:
                    title = item.a.string # 获取文章标题
                    link = item.a.get('href') # 获取文章链接
                    link = BaseFeedBook.urljoin(url, link) # 合成文章链接
                    urls.append((topic, title, link, None)) # 把文章元组加入列表
            # 如果请求失败通知到日志输出中
            else:
                self.log.warn('Fetch article failed(%s):%s' % \
                    (URLOpener.CodeMap(result.status_code), url))
        # 返回提取到的所有文章列表
        return urls