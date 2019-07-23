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
        (u'纽约时报', 'https://cn.nytimes.com/rss/'),
    ]
    
    # fulltext_by_readability = False
    
    keep_only_tags = [
        dict(name='div', class_='article-header'),
        dict(name='div', class_='article-paragraph'),
    ]
    
    max_articles_per_feed = 20 # 设定每个主题下要最多可抓取的文章数量

def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """
        urls = []
        tnow = datetime.datetime.utcnow()
        urladded = set()
        
        for feed in self.feeds:
            section, url = feed[0], feed[1]
            isfulltext = feed[2] if len(feed) > 2 else False
            timeout = self.timeout+10 if isfulltext else self.timeout
            opener = URLOpener(self.host, timeout=timeout, headers=self.extra_header)
            result = opener.open(url)
            if result.status_code == 200 and result.content:
                #debug_mail(result.content, 'feed.xml')
                decoder = AutoDecoder(isfeed=True)
                content = self.AutoDecodeContent(result.content, decoder, self.feed_encoding, opener.realurl, result.headers)
                
                feed = feedparser.parse(content)
                
                for e in feed['entries'][:self.max_articles_per_feed]:
                    updated = None
                    if hasattr(e, 'updated_parsed') and e.updated_parsed:
                        updated = e.updated_parsed
                    elif hasattr(e, 'published_parsed') and e.published_parsed:
                        updated = e.published_parsed
                    elif hasattr(e, 'created_parsed'):
                        updated = e.created_parsed
                    
                    if self.oldest_article > 0 and updated:
                        updated = datetime.datetime(*(updated[0:6]))
                        delta = tnow - updated
                        if self.oldest_article > 365:
                            threshold = self.oldest_article #以秒为单位
                        else:
                            threshold = 86400*self.oldest_article #以天为单位
                        
                        if delta.days*86400+delta.seconds > threshold:
                            self.log.info("Skip old article(%s): %s" % (updated.strftime('%Y-%m-%d %H:%M:%S'), e.link))
                            continue
                    
                    title = e.title if hasattr(e, 'title') else 'Untitled'
                    
                    #支持HTTPS
                    if hasattr(e, 'link'):
                        if url.startswith('https://'):
                            urlfeed = e.link.replace('http://','https://')
                        else:
                            urlfeed = e.link
                            
                        if urlfeed in urladded:
                            continue
                    else:
                        urlfeed = ''
                    
                    desc = None
                    if isfulltext:
                        summary = e.summary if hasattr(e, 'summary') else None
                        desc = e.content[0]['value'] if (hasattr(e, 'content')
                            and e.content[0]['value']) else None

                        #同时存在，因为有的RSS全文内容放在summary，有的放在content
                        #所以认为内容多的为全文
                        if summary and desc:
                            desc = summary if len(summary) > len(desc) else desc
                        elif summary:
                            desc = summary

                        if not desc:
                            if not urlfeed:
                                continue
                            else:
                                self.log.warn('Fulltext feed item no has desc,link to webpage for article.(%s)' % title)
                    
                    urladded.add(urlfeed)
                    #针对URL里面有unicode字符的处理，否则会出现Bad request
                    #后面参数里面的那一堆“乱码”是要求不处理ASCII的特殊符号，只处理非ASCII字符
                    urlfeed = urllib.quote_plus(urlfeed.encode('utf-8'), r'''~`!@#$%^&*()|\\/,.<>;:"'{}[]?=-_+''')
                    urls.append((section, title, urlfeed, desc))
            else:
                self.log.warn('fetch rss failed(%s):%s' % (URLOpener.CodeMap(result.status_code), url))
                
        return urls
