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

import main

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    # ermöglicht multithreading
    pass


class HTTPServerV6(ThreadingMixIn, HTTPServer):
    address_family = socket.AF_INET6


class SmallServer(BaseHTTPRequestHandler):

    def do_GET(self):

        # ./smallserver/transaktion.html -> letzter teil ist get parameter
        filedir = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))
        file = os.path.join(filedir, basename(urlsplit(self.path).path))
        # dateien mit bzw. ohne query zurückgeben
        onlyFilename = basename(urlsplit(self.path).path)
        # typ des files bestimmen
        mimetype, fileencoding = mimetypes.guess_type(onlyFilename)
        print(file)
        with open(file, 'rb') as html_file:
            # le parsing
            modified_page = BeautifulSoup(html_file, "html.parser")
            powertags = modified_page.find_all('p', {'name': 'Power'})
            for Tag in powertags:
                Tag.string = str(xbox.output_power)

        if onlyFilename not in ['favicon.ico', 'myStyle.css']:
            parameter = parse_qs(urlparse(self.path).query)
            print(parameter)
            self.send_response(200)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(modified_page.encode())
        else:
            with open(file, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(file.read())


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
    xbox = main.Controller(pollingrate=0.2)
    run('ipv4', 8081)

