from search_engine.lib.decorators import singleton
from search_engine.index.page import Page
import urlparse, collections, threading

@singleton
class Index:
    def __init__(self):
        self._index = {}
        self._pages = {}
        self._hosts = []
        self._depth = collections.Counter()
        self._locker = threading.Lock()

    def clear(self):
        self._locker.acquire()
        try:
            self._index = {}
            self._pages = {}
            self._hosts = []
            self._depth = collections.Counter()
        finally:
            self._locker.release()


    def add_page(self, url, depth):
        self._locker.acquire()
        try:
            if url not in self._pages:
                self._pages[url] = Page(url)
                self._depth[depth] += 1
                
                r = urlparse.urlsplit(url)
                if r.hostname not in self._hosts:
                    self._hosts.append(r.hostname)
        finally:
            self._locker.release()

    def add(self ,key, url):
        self._locker.acquire()
        try:
            key = key.lower()
            
            if key in self._index:
                documents = self._index[key]
                if url not in documents:
                    documents.append(url)    
            else:
                self._index[key] = [url]
        finally:
            self._locker.release()


    def lookup(self, key):
        key = key.lower()
        if key in self._index:
            return self._index[key]
        else:
            return []

    def has_page(self, url):
        return url in self._pages

    def len(self):
        return len(self._index), len(self._pages), len(self._hosts)

    def hosts(self):
        self._locker.acquire()
        try:
            return self._hosts
        finally:
            self._locker.release()

    def get_depth_stat(self):
        self._locker.acquire()
        try:
            items = self._depth.items()
            items.sort()
            return items
        finally:
            self._locker.release()

    def most_common(self, cnt):
        self._locker.acquire()
        try:
            c = collections.Counter()
            for key in self._index:
                c[key] = len(self._index[key])
            return c.most_common(cnt)
        finally:
            self._locker.release()

    
