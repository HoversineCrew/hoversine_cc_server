#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import mimetypes
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlsplit
from posixpath import basename

from bs4 import BeautifulSoup


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    # ermöglicht multithreading
    pass


class SmallServer(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # ./smallserver/transaktion.html -> letzter teil ist get parameter
            filedir = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))
            file = os.path.join(filedir, basename(urlsplit(self.path).path))
            # dateien mit bzw. ohne query zurückgeben
            onlyFilename = basename(urlsplit(self.path).path)
            # typ des files bestimmen
            mimetype, fileencoding = mimetypes.guess_type(onlyFilename)
            print(file)
            if onlyFilename not in ['favicon.ico', 'myStyle.css']:
                parameter = parse_qs(urlparse(self.path).query)
                print(parameter)
                with open(file, 'rb') as html_file:
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(html_file.read())
            else:
                with open(file, 'rb') as html_file:
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(html_file.read())
        except:
            print("error")


class HTTPServerV6(ThreadingMixIn, HTTPServer):
    address_family = socket.AF_INET6


def run(ip_version, port):

    if ip_version == 'ipv4':
        server_address = ('', port)
        httpd = ThreadingSimpleServer(server_address, SmallServer)

    elif ip_version == 'ipv6':
        server_address = ('::', port)
        httpd = HTTPServerV6(server_address, SmallServer)
    else:
        raise NameError("Please provide ipv4 or ipv6 as value")

    try:
        httpd.serve_forever()
    except:
        httpd.socket.close()

if __name__ == '__main__':
    run('ipv4', 8081)

