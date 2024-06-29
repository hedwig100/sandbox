from http.server import HTTPServer, BaseHTTPRequestHandler
from requests_toolbelt.multipart import decoder


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def parse_multipart(self):
        content_length = int(self.headers["Content-Length"])
        multipart_decoder = decoder.MultipartDecoder(
            self.rfile.read(content_length),
            self.headers["Content-Type"],
        )
        return multipart_decoder.parts

    def do_POST(self):
        ## Parse request
        multiparts = self.parse_multipart()

        print(multiparts[0].headers)
        print(multiparts[0].content[:20])

        ## Return response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("Successful\n".encode())


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ("localhost", 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run(handler_class=HTTPRequestHandler)
