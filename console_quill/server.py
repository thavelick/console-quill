#!/usr/bin/env python3

import argparse
import json
import os
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


class ConsoleQuillHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, logfile_path=None, **kwargs):
        self.logfile_path = logfile_path
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/console-quill.js':
            self.serve_javascript()
        elif path == '/':
            self.serve_status()
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/log':
            self.handle_log()
        else:
            self.send_error(404, "Not Found")

    def serve_javascript(self):
        js_path = os.path.join(os.path.dirname(__file__), 'static', 'console-quill.js')
        try:
            with open(js_path, 'r') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content.encode())
        except FileNotFoundError:
            self.send_error(404, "JavaScript file not found")

    def serve_status(self):
        status_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Console Quill Status</title>
        </head>
        <body>
            <h1>Console Quill Server</h1>
            <p>Server is running and ready to receive console logs.</p>
            <p>Include this script in your HTML page:</p>
            <code>&lt;script src="http://localhost:{port}/console-quill.js"&gt;&lt;/script&gt;</code>
        </body>
        </html>
        """.format(port=self.server.server_port)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(status_html.encode())

    def handle_log(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            log_data = json.loads(post_data.decode())
            
            timestamp = datetime.now().isoformat()
            level = log_data.get('level', 'log')
            message = log_data.get('message', '')
            
            log_entry = {
                'timestamp': timestamp,
                'level': level,
                'message': message
            }
            
            with open(self.logfile_path, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            
        except Exception as e:
            self.send_error(500, f"Error logging message: {str(e)}")

    def log_message(self, format, *args):
        pass


def create_handler(logfile_path):
    def handler(*args, **kwargs):
        return ConsoleQuillHandler(*args, logfile_path=logfile_path, **kwargs)
    return handler


def main():
    parser = argparse.ArgumentParser(description='Console Quill - Capture console.log messages from web pages')
    parser.add_argument('--logfile', required=True, help='Path to the log file')
    parser.add_argument('--port', type=int, default=9876, help='Port to run the server on (default: 9876)')
    
    args = parser.parse_args()
    
    handler = create_handler(args.logfile)
    
    try:
        server = HTTPServer(('localhost', args.port), handler)
        print(f"Console Quill server running on http://localhost:{args.port}")
        print(f"Logging to: {args.logfile}")
        print(f"Include this script in your HTML: <script src=\"http://localhost:{args.port}/console-quill.js\"></script>")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()