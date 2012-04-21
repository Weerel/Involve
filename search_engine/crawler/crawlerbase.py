from search_engine.index.api import IndexManager
from search_engine.crawler.parser import Parser
from search_engine.crawler.linkqueue import LinkQueue
import urllib, time, threading, logging

class CrawlerBase:
    def __init__(self, config):
        self._index = IndexManager.get_proxy()
        self._parser = Parser()
        self._tocrawl = LinkQueue(self._index)
        self._tocrawl.extend(config.seed)
        self._thread_count = config.thread_count
        self._delay = config.delay
   
class CrawlerWorkerBase(threading.Thread):
    def __init__(self, tocrawl, index, parser, delay):
        threading.Thread.__init__(self)
        self._tocrawl = tocrawl
        self._delay = delay
        self._index = index
        self._parser = parser

    def get_url(self):
        return self._tocrawl.get()        

    def get_page(self ,url):
        f = urllib.urlopen(url)
        page = f.read()
        f.close()
        self._index.add_page(url)
        return page

    def add_page_to_index(self, url, page):
        words = self._parser.get_words(page)
        for word in words:
            self._index.add(word, url)

    def update_links(self, content, url):
        self._tocrawl.extend(self._parser.get_links(content, url))

    def need_crawl(self):
        return not self._tocrawl.empty()

    def done(self):
        self._tocrawl.done()

    def sleep(self):
        time.sleep(self._delay)

    def run(self):
        logging.debug('start')
        while self.need_crawl():
            try:
                url = self.get_url()
            except IndexError:
                logging.debug('IndexError %s %s', self._tocrawl._count, self._tocrawl._count_done)                
            else:
                try:                    
                    page = self.get_page(url)                    
                    self.add_page_to_index(url, page)
                    self.update_links(page, url)
                except Exception as ex:
                    logging.exception(ex)
                finally:
                    self.done()
            self.sleep()
        logging.debug('end')
