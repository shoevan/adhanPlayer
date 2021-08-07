#!/usr/bin/env python

import time
import os
import http.server
import socketserver

def startHttpServer():
    os.chdir(os.getenv("HOME"))
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port ", PORT)
        httpd.serve_forever()

def main(): 
    startHttpServer()

if __name__ == "__main__":
    main()
