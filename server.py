
import http.server
import socketserver
import json
import os
import subprocess
from urllib.parse import urlparse, parse_qs

PORT = 8080
ROOT_DIR = "/Users/dkmac/Desktop/@26/dev"
WEB_DIR = "/Users/dkmac/Desktop/@26/dev/_ops/web"

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url_path = urlparse(self.path)
        if url_path.path == '/api/open':
            query = parse_qs(url_path.query)
            file_name = query.get('file', [None])[0]
            if file_name:
                # Find the file path
                found_path = None
                for r, d, f in os.walk(ROOT_DIR):
                    if file_name in f:
                        found_path = os.path.join(r, file_name)
                        break
                
                if found_path:
                    subprocess.run(["open", found_path])
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"OK")
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"File Not Found")
            return
        
        # Default behavior: serve static files from WEB_DIR
        os.chdir(WEB_DIR)
        return super().do_GET()

os.chdir(WEB_DIR)
with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
