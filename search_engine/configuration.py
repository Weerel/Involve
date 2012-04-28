import logging

class Configuration:
    class WebServerConfig:
        webdir = '.\web'
        port = 80
        host = 'localhost'
    class CrawlerConfig:
        seed = ('http://www.bbc.com/',)
        #seed = ('http://localhost/cgi-bin/web.py?d=20&d=10&d=2&v=0&v=0&v=0',)
        thread_count = 2
        delay = 1
        loaded_pages_queue_size = 20
        index_pages = True


logging.basicConfig(filename='search_engine.log', format='%(threadName)s %(message)s', level=logging.INFO)
#logging.basicConfig(format='%(threadName)s %(message)s', level=logging.INFO)
