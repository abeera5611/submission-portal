from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os

TOKEN = os.getenv("REPORT_TOKEN", "secret")

class H(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.headers.get("X-Token") != TOKEN:
            self.send_response(401); self.end_headers(); return
        body = self.rfile.read(int(self.headers["Content-Length"]))
        json.dump(json.loads(body), open("test-report.json", "w"), indent=2)
        self.send_response(200); self.end_headers(); self.wfile.write(b"saved")

HTTPServer(("0.0.0.0", 8000), H).serve_forever()