class Page:
    def __init__(self, url):
        self._url = url
        self._rank = 0
        self._date = None
        self._links = {}

    def add_link(self, page):
        if page._url not in self._links:
            self._links[page._url] = page

    def remove_link(self, page):
        pass
