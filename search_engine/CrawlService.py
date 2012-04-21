from multiprocessing import freeze_support
from search_engine.crawler.threadcrawler import ThreadCrawler
from search_engine.crawler.processcrawler import ProcessCrawler
from configuration import Configuration
import logging, socket

config = Configuration.CrawlerConfig

if __name__ == '__main__':
    freeze_support()
    logging.info('starting CrawlService')
    try:
        crawler = ProcessCrawler(config)
        #crawler = ThreadCrawler(config)
        crawler.run()
    except socket.error:
        logging.error("can't connect to DataStorage")
