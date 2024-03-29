from search_engine.crawler.crawlerbase import CrawlerBase, CrawlerWorkerBase
import threading, logging

class ThreadCrawler(CrawlerBase):
    def __init__(self, config):
        CrawlerBase.__init__(self, config)
   
    def run(self):
        for i in range(self._thread_count):
            worker = ThreadCrawlerWorker(self._tocrawl, self._index, self._parser, self._delay, self._index_pages)            
            worker.start()

class ThreadCrawlerWorker(CrawlerWorkerBase, threading.Thread):
    def __init__(self, tocrawl, index, parser, delay, index_pages):
        CrawlerWorkerBase.__init__(self, tocrawl, index, parser, delay, index_pages)
        self.daemon = False

    def run(self):
        logging.debug('start')
        while self.need_crawl():
            try:
                url, depth = self.get_url()
                logging.info('%s %s %s', self._tocrawl._count, self._tocrawl._count_done , url)
            except IndexError:
                logging.debug('IndexError %s %s', self._tocrawl._count, self._tocrawl._count_done)                
            else:
                try:                    
                    page = self.get_page(url, depth)                    
                    self.add_page_to_index(url, page)
                    self.update_links(page, url, depth)
                except Exception as ex:
                    logging.exception(ex)
                finally:
                    self.done(url)
            self.sleep()
        logging.debug('end')
