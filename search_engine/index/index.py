from search_engine.lib.decorators import singleton
from search_engine.index.page import Page
import urlparse, collections

@singleton
class Index:
    def __init__(self):
        self._index = {}
        self._pages = {}
        self._hosts = []

    def add_page(self, url):
        if url not in self._pages:
            self._pages[url] = Page(url)
            
        r1 = urlparse.urlsplit(url)
        if r1.hostname not in self._hosts:
            self._hosts.append(r1.hostname)


    def add(self ,key, url):        
        self.add_page(url)
        key = key.lower()
        
        if key in self._index:
            documents = self._index[key]
            if url not in documents:
                documents.append(url)    
        else:
            self._index[key] = [url]

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
        return self._hosts

    def most_common(self, cnt):
        c = collections.Counter()
        for key in self._index:
            c[key] = len(self._index[key])
        return c.most_common(cnt)
    
