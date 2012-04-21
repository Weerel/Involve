import logging

class Configuration:
    class WebServerConfig:
        webdir = '.\web'
        port = 80
        host = 'localhost'
    class CrawlerConfig:
        #seed = ('http://www.bbc.com/',)
        seed = ('http://localhost/cgi-bin/web.py?d=3&d=3&d=3&v=0&v=0&v=0',)
        thread_count = 5
        delay = 0.2
        loaded_pages_queue_size = 20
        

#filename='example.log'
logging.basicConfig(format='%(threadName)s %(message)s', level=logging.DEBUG)
