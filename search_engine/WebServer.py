import os, sys, logging
from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
from configuration import Configuration

config = Configuration.WebServerConfig

class CustomHandler(CGIHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header("Location", "/cgi-bin/index.py")
            self.end_headers()            
        else:
            CGIHTTPRequestHandler.do_GET(self)

if sys.platform[:3] == 'win':
    CGIHTTPRequestHandler.have_popen2 = False
    CGIHTTPRequestHandler.have_popen3 = False

if __name__ == '__main__':
    logging.info('starting WebServer host=%s:%s', config.host, config.port)
    os.chdir(config.webdir)
    server = HTTPServer((config.host, config.port), CustomHandler)
    server.serve_forever()
