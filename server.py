from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse
import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 5050

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path == "/query":
            query = urllib.parse.parse_qs(parsed_path.query).get("q", [""])[0]

            try:
                result = subprocess.run(
                    ["python", "main.py", query],
                    cwd=BASE_DIR,
                    capture_output=True,
                    text=True
                )

                if result.returncode != 0:
                    self.send_response(500)
                    self.send_header("Content-type", "text/plain; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    error_text = result.stderr.strip() if result.stderr else "Backend error"
                    self.wfile.write(error_text.encode("utf-8"))
                    return

                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(result.stdout.encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(str(e).encode("utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"Endpoint not found")

    def log_message(self, format, *args):
        # Keep default logging concise
        print("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format % args))

server = ThreadingHTTPServer(("localhost", 5050), SimpleHandler)
print(f"Server running on http://localhost:{5050}")
server.serve_forever()