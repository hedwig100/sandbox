import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler


if __name__ == "__main__":
    out = sys.stderr

    out.write(f"arguments: {sys.argv}\n")
    out.write(f"environments: {[(k, os.getenv(k)) for k in os.environ]}\n")

    host = os.getenv("TINYHTTPD_HOST", "")
    port = os.getenv("TINYHTTPD_PORT", 8000)
    listen = (host, int(port))
    httpd = HTTPServer(listen, SimpleHTTPRequestHandler)

    out.write(f"listen: host={listen[0]}, port={listen[1]}\n")

    httpd.serve_forever()