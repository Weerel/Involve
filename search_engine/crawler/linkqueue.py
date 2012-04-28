import collections, threading

class LinkQueue:
    def __init__(self, index):
        self._count = 0
        self._count_done = 0
        self._queue = collections.deque()
        self._depth_queue = collections.deque()
        self._index = index
        self._locker = threading.Lock()
        self._loaging_pages = collections.deque()

    def _put(self, url, depth):
        #if url not in self._queue and url not in self._loaging_pages and not self._index.has_page(url):
        if url not in self._queue and url not in self._loaging_pages:
            self._queue.append(url)
            self._depth_queue.append(depth)
            self._count += 1                
            self._count_done += 1

    def extend(self, urls, current_depth):
        self._locker.acquire()
        try:
            for url in urls:                
                self._put(url, current_depth + 1)
        finally:
            self._locker.release()

    def get(self):
        self._locker.acquire()
        try:
            url = self._queue.popleft()
            depth = self._depth_queue.popleft()
            self._loaging_pages.append(url)
            self._count -= 1
            return url, depth
        finally:
            self._locker.release()

    def done(self, url):
        self._locker.acquire()
        try:
            self._count_done -= 1
            #if url in self._loaging_pages:
                #self._loaging_pages.remove(url)
        finally:
            self._locker.release()


    def empty(self):
        return self._count_done <= 0
