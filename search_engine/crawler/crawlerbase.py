from search_engine.index.api import IndexManager
from search_engine.crawler.parser import Parser
from search_engine.crawler.linkqueue import LinkQueue
import urllib, time, threading, logging

class CrawlerBase:
    def __init__(self, config):
        self._index = IndexManager.get_proxy()
        self._index.clear()
        self._parser = Parser()
        self._tocrawl = LinkQueue(self._index)
        self._tocrawl.extend(config.seed, -1)
        self._thread_count = config.thread_count
        self._delay = config.delay
        self._index_pages = config.index_pages
   
class CrawlerWorkerBase(threading.Thread):
    def __init__(self, tocrawl, index, parser, delay, index_pages):
        threading.Thread.__init__(self)
        self._tocrawl = tocrawl
        self._delay = delay
        self._index = index
        self._parser = parser
        self._index_pages = index_pages

    def get_url(self):
        return self._tocrawl.get()        

    def get_page(self ,url, depth):
        f = urllib.urlopen(url)
        page = f.read()
        f.close()
        self._index.add_page(url, depth)
        return page

    def add_page_to_index(self, url, page):
        if self._index_pages:
            words = self._parser.get_words(page)
            for word in words:
                self._index.add(word, url)

    def update_links(self, content, url, current_depth):
        self._tocrawl.extend(self._parser.get_links(content, url), current_depth)

    def need_crawl(self):
        return not self._tocrawl.empty()

    def done(self, url):
        self._tocrawl.done(url)

    def sleep(self):
        time.sleep(self._delay)
