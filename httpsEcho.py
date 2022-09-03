import sys
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer

class Server(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

        print(f"{self.headers}", end="")
        print("--------------------------------------------------------------------------------------------------------------\n")

    def do_POST(self):
        if self.headers["Content-Length"]:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
        else:
            post_data = b""

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))

        print(f"{self.headers}", end="")
        print(f"{post_data.decode('utf-8')}\n")
        print("--------------------------------------------------------------------------------------------------------------\n")


def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./cert.pem', server_side=True)
    print("Starting https server on "+ str(port) + " ...\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Stopping https server ...\n")


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()