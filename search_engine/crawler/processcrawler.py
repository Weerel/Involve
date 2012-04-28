from search_engine.crawler.crawlerbase import CrawlerBase, CrawlerWorkerBase
from multiprocessing import Process, Queue
import threading, logging, time

class Counter:
    def __init__(self, tocrawl):
        self._tocrawl = tocrawl
        
        self._loading = 0
        self._waiting = 0
        self._indexing = 0
        self._indexed = 0
        
        self._start_time = 0
        self._indexing_time = 0
        self._start_index_time = 0
        self._index_time = 0

    def start(self):
        self._start_time = time.time()

    def page_start_load(self):
        self._loading += 1

    def page_end_load(self, url):
        self._loading -= 1
        self._waiting += 1
        logging.debug('time:%f, url:%s', time.time()-self._start_time, url)

    def page_err_load(self, url):
        self._loading -= 1
        logging.error("time:%f, can't load: %s",time.time()-self._start_time, url)

    def page_start_index(self):
        self._waiting -= 1
        self._indexing += 1
        self._start_index_time = time.time()

    def page_end_index(self):
        self._indexing -= 1
        self._indexed += 1
        self._index_time = time.time() - self._start_index_time
        self._indexing_time += self._index_time


    def log(self, depth):
        logging.info('time total:%f, indexing:%f, last_index:%f', time.time()-self._start_time, self._indexing_time, self._index_time)
        logging.info('loading:%i, waiting:%i, indexed:%i, depth:%i, links:%i', self._loading, self._waiting, self._indexed, depth, self._tocrawl._count)
        

class ProcessCrawler(CrawlerBase):
    def __init__(self, config):
        logging.info('seed=%s, thread_count=%s, delay=%f, queue_size=%i', config.seed, config.thread_count, config.delay, config.loaded_pages_queue_size)
        CrawlerBase.__init__(self, config)
        self._queue = Queue(config.loaded_pages_queue_size)
        self._counter = Counter(self._tocrawl)
        self._indexer = IndexingWorker(self._tocrawl, self._index, self._parser, self._delay, self._queue, self._counter, self._index_pages)        
   
    def run(self):
        self._counter.start()
        for i in range(self._thread_count):
            downloader = DownloadWorker(self._tocrawl, self._index, self._parser, self._delay, self._queue, self._counter,  self._index_pages)
            downloader.name = 'downloading_' + str(i)
            downloader.start()
        self._indexer.start()

class DownloadWorker(CrawlerWorkerBase, threading.Thread):
    def __init__(self, tocrawl, index, parser, delay, queue, counter, index_pages):
        CrawlerWorkerBase.__init__(self, tocrawl, index, parser, delay, index_pages)
        self._queue = queue
        self._counter = counter
        self.daemon = False

    def run(self):
        logging.debug('start')
        while self.need_crawl():
            try:
                url, depth = self.get_url()
            except IndexError:
                logging.debug('IndexError')                
            else:
                try:
                    self._counter.page_start_load()
                    page = self.get_page(url, depth)                    
                    self._queue.put((url, page, depth))
                    self._counter.page_end_load(url)
                except IOError:
                    self.done(url)
                    self._counter.page_err_load(url)
                except Exception as ex:
                    logging.exception(ex)
            self.sleep()
        logging.debug('end')

class IndexingWorker(CrawlerWorkerBase, Process):
    def __init__(self, tocrawl, index, parser, delay, queue, counter, index_pages):
        CrawlerWorkerBase.__init__(self, tocrawl, index, parser, delay, index_pages)
        self._queue = queue
        self._counter = counter
        self.name = 'indexing'

    def run(self):
        logging.debug('start')
        while self.need_crawl():
            try:
                url, page, depth = self._queue.get()
            except IndexError:
                logging.debug('IndexError')
            else:
                try:
                    self._counter.page_start_index()
                    self.add_page_to_index(url, page)
                    self.update_links(page, url, depth)
                    self._counter.page_end_index()                    
                    self._counter.log(depth)
                except Exception as ex:
                    logging.exception(ex)
                finally:
                    self.done(url)
        logging.debug('end')
