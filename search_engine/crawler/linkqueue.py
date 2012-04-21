import collections, threading

class LinkQueue:
    def __init__(self, index):
        self._count = 0
        self._count_done = 0
        self._queue = collections.deque()
        self._index = index
        self._locker = threading.Lock()
        self.n = 0

    def _put(self, url):
        if self._queue.count(url) == 0 and not self._index.has_page(url):
            self._queue.append(url)            
            self._count += 1                
            self._count_done += 1
            self.n += 1

    def extend(self, urls):
        self._locker.acquire()
        try:
            for url in urls:                
                self._put(url)
        finally:
            self._locker.release()

    def get(self):
        self._locker.acquire()
        try:
            val = self._queue.popleft()
            self._count -= 1
            return val
        finally:
            self._locker.release()

    def done(self):
        self._count_done -= 1        

    def empty(self):
        return self._count_done <= 0
