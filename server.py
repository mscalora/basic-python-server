#!/usr/bin/env python

from __future__ import print_function, with_statement

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json


class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self, content_type='text/html', http_status=200, headers={}):
        self.send_response(http_status)
        if content_type is not None:
            self.send_header('Content-type', content_type)
        for header, value in headers.iteritems():
            self.send_header(header, value)
        self.end_headers()

    def _send_file(self, the_file, content_type='text/html'):
        self._set_headers(content_type=content_type)
        if hasattr(the_file, 'read'):
            data = the_file.read()
        else:
            with open(the_file, 'r') as f:
                data = f.read()
        self.wfile.write(data)

    def _send_json(self, data_object={}):
        self._set_headers('application/json', 200)
        json.dump(data_object, self.wfile)

    def do_GET(self):
        self._send_file("index.html")

    def do_HEAD(self):
        self._set_headers(content_type=None)

    def do_POST(self):
        action = self.path.lstrip('/').split('/')[0]
        if len(action) == 0:
            self._send_json({"error": False})
        elif hasattr(self, action):
            getattr(self, action)()
        else:
            self._set_headers(http_status=404, content_type=None)

    def ping(self):
        self._send_json({"response": "pong"})


def run(server_class=HTTPServer, handler_class=MyServer, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port %d' % port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")

if __name__ == "__main__":
    from sys import argv


if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()
