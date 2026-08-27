#!/usr/bin/env python3
"""Serve punish.html and receive the spare/kill verdict. Usage: punish-server.py <port> <dir>"""
import http.server, os, sys, threading

PORT, DIR = int(sys.argv[1]), sys.argv[2]

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=DIR, **k)

    def do_GET(self):
        if self.path == '/will':
            p = os.path.join(DIR, 'handoff.md')
            if os.path.exists(p):
                data = open(p, 'rb').read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/markdown; charset=utf-8')
                self.send_header('Cache-Control', 'no-store')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_response(404)
                self.end_headers()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/verdict':
            n = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(n)
            with open(os.path.join(DIR, 'verdict.json'), 'wb') as f:
                f.write(body)
            self.send_response(204)
            self.end_headers()
            threading.Timer(1.0, lambda: os._exit(0)).start()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *a):
        pass

http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
