import re, urlparse

class Parser:
    _re_links = re.compile('<a href=\"([^\"]*)\">.*<\/a>')
    _re_content = re.compile('<[^<]*?/?>')
    _re_special_entities = re.compile('&nbsp;|&amp;')
    _re_words = re.compile("[a-z0-9_]+", re.IGNORECASE)
    _link_filter = ("mailto:", "javascript:")
    _tags_to_remove = ('head', 'script', 'xml', 'style')  

    def __init__(self):
        self._re_tags_to_remove = [re.compile('<' + tag + '.*?>(.|\n)*?</' + tag + '>', re.IGNORECASE) for tag in self._tags_to_remove]  

    def _normalize_url(self, url):
        if url == '' or url[0] == '#':
            return ''
 
        #add default scheme for absolute url
        if url[0] not in ('/', '-', '.') and url.find('://') == -1:
            url = 'http://' + url
           
        #split url
        scheme, auth, path, query, fragment = urlparse.urlsplit(url.strip())
        
        #convert the scheme and host to lower case
        scheme = scheme.lower()
        auth = auth.lower()
        path = path.lower()

        #add trailing
        if path == '':
            path = '/'    

        #combine url and remove the fragment    
        return urlparse.urlunsplit((scheme, auth, path, query, ''))

    def _check_link(self, url):
        for condition in self._link_filter:
            if url.find(condition) == 0:
                return False
        return True

    def _strip_tags(self, html):
        html = self._re_content.sub('', html)
        return self._re_special_entities.sub(' ', html)                    

    def _get_text(self, html):
        for r in self._re_tags_to_remove:
            html = r.sub('', html)
        return self._strip_tags(html)

    def get_links(self, html, base_url):
        for url in self._re_links.findall(html):
            if self._check_link(url):
                url = self._normalize_url(url)
                if url not in ('', base_url):
                    #convert relative url to absolute and remove dot-segments
                    url = urlparse.urljoin(base_url, url)
                    yield url

    def get_words(self, html):
        text = self._get_text(html)
        return self._re_words.findall(text)
