#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cController
import os
import mimetypes
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlsplit
from posixpath import basename


# controller global so it is not instanciated multiple times
xbox = cController.Controller(pollingrate=0.2)


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    # ermöglicht multithreading
    pass


class SmallServer(BaseHTTPRequestHandler):

    def do_GET(self):

        # ./smallserver/transaktion.html -> letzter teil ist get parameter
        filedir = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))
        file = os.path.join(filedir, basename(urlsplit(self.path).path))
        # dateien mit bzw. ohne query zurückgeben
        only_filename = basename(urlsplit(self.path).path)
        # typ des files bestimmen
        mimetype, fileencoding = mimetypes.guess_type(only_filename)

        with open(file, 'r') as html_file:
            html = html_file.read()
            html = html.replace("@Motor1", str(xbox.outputs[0]/10))
            html = html.replace("@Motor2", str(xbox.outputs[1]/10))


        if only_filename not in ['favicon.ico', 'gauge.css']:
            # parameter = parse_qs(urlparse(self.path).query)
            self.send_response(200)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            with open(file, 'rb') as html_file:
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(html_file.read())


def run(port):

    server_address = ('', port)
    httpd = ThreadingSimpleServer(server_address, SmallServer)

    try:
        httpd.serve_forever()
    except:
        httpd.socket.close()


if __name__ == '__main__':

    run(8081)

