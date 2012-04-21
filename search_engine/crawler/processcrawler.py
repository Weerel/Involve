from search_engine.crawler.crawlerbase import CrawlerBase, CrawlerWorkerBase
from multiprocessing import Process, Queue
import threading, logging, time

class ProcessCrawler(CrawlerBase):
    def __init__(self, config):
        logging.info('seed=%s, thread_count=%s, delay=%f, queue_size=%i', config.seed, config.thread_count, config.delay, config.loaded_pages_queue_size)
        CrawlerBase.__init__(self, config)
        self._queue = Queue(config.loaded_pages_queue_size)
        self._indexer = IndexingWorker(self._tocrawl, self._index, self._parser, self._delay, self._queue)        
   
    def run(self):                
        for i in range(self._thread_count):
            downloader = DownloadWorker(self._tocrawl, self._index, self._parser, self._delay, self._queue)
            downloader.name = 'downloading_' + str(i)
            downloader.start()
        self._indexer.start()

class DownloadWorker(CrawlerWorkerBase, threading.Thread):
    def __init__(self, tocrawl, index, parser, delay, queue):
        CrawlerWorkerBase.__init__(self, tocrawl, index, parser, delay)
        self._queue = queue
        self.daemon = False

    def run(self):
        logging.debug('start')
        while self.need_crawl():
            try:
                url = self.get_url()
            except IndexError:
                logging.debug('IndexError')                
            else:
                try:
                    page = self.get_page(url)
                    self._queue.put((url, page))
                    logging.debug(url[-10:-1].replace('&v=',''))
                except IOError:
                    self.done()
                    logging.error("can't load %s", url)
                except Exception as ex:
                    logging.exception(ex)
            self.sleep()
        logging.debug('end')

class IndexingWorker(CrawlerWorkerBase, Process):
    def __init__(self, tocrawl, index, parser, delay, queue):
        CrawlerWorkerBase.__init__(self, tocrawl, index, parser, delay)
        self._queue = queue
        self._count = 0
        self.name = 'indexing'

    def run(self):
        logging.debug('start')
        while self.need_crawl():
            try:
                url, page = self._queue.get()
            except IndexError:
                logging.debug('IndexError')
            else:
                try:
                    self.add_page_to_index(url, page)
                    self.update_links(page, url)
                    self._count += 1
                    
                    #log statistic
                    loaded_cnt = self._queue.qsize()
                    loading_cnt = self._tocrawl._count_done - self._tocrawl._count - loaded_cnt
                    n_cnt =  self._tocrawl.n                  
                    logging.info('indexed:%i, to_be_indexed:%i, loading:%i, links:%i', self._count, loaded_cnt, loading_cnt,  self._tocrawl._count)
                    logging.info('n_q:%i, n_i:%i', n_cnt, self._index.len()[1])
                except Exception as ex:
                    logging.exception(ex)
                finally:
                    self.done()
        logging.debug('end')
