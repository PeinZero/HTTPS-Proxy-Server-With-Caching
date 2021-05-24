import http.server
import socketserver
import urllib.request
import shutil
import os
import hashlib
import sys
import requests
from get_webpage import savePage
import codecs
import webbrowser

BLOCKED = ['https://downloadly.net']

class CacheHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = self.path[1:]
        
        if url in BLOCKED:
            self.send_response(403)
            self.end_headers()
            return

        pos1 = url.find('://')
        pos2 = url.find('.')
        name  = url[pos1+3:]
        if not os.path.exists(name+".html"):
            soup = savePage(url, name)
        else:
            print("cache hit")

        
        # f=codecs.open(name + '.html', 'r', encoding="utf-8")
        # self.send_response(200)
        # self.end_headers()
        # self.wfile.write(bytes(f.read(), "utf-8"))
        # f.close()
        webbrowser.open(name+".html")
        input()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", 5555), CacheHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)