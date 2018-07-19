import socket as s
from io import StringIO
import sys


class WSGIServer:

    request_queue_size = 1

    def __init__(self, server_addr):
        # Create a listening socket
        self.listen_socket = listen_socket = s.socket()

        # Allow reuse of the same address
        listen_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        # Bind
        listen_socket.bind(server_addr)
        # Activate
        listen_socket.listen(self.request_queue_size)
        host, port = listen_socket.getsockname()[:2]

        self.server_name = s.getfqdn(host)
        self.server_port = port
        # Return headers set by Web framework/Web application
        self.headers_set = []

    def set_app(self, application):
        self.application = application

    def run(self):
        listen_socket = self.listen_socket
        while True:
            # New client connection
            self.client_connection, client_address = listen_socket.accept()
            # Handle one request and close the client connection
            # Then loop over to wait for another client connection
            self.handle_one_request()

    def handle_one_request(self):
        self.request_data = request_data = self.client_connection.recv(1024)
        # print formatted request data a la 'curl -v'
        print(''.join('< {line}\n'.format(line=line)
                      for line in request_data.splitlines()))

        self.parse_request(request_data)

        # Construct environment dictionary using request data
        env = self.get_environ()

        # call our application callable and get back
        # a result that will become HTTP response body
        result = self.application(env, self.start_response)
        print(result)
        self.finish_response(result)

    def parse_request(self, text):
        request_line = text.splitlines()[0].decode('utf8')
        request_line = request_line.rstrip('\r\n')
        # Break down the request line into components
        (self.request_method,   # GET
         self.path,              # /hello
         self.request_version    # HTTP/1.1
        ) = request_line.split()

    def get_environ(self):
        env = {
            # Required WSGI variables
            'wsgi.version':         (1, 0),
            'wsgi.url_scheme':      'http',
            'wsgi.input':           StringIO(self.request_data.decode('utf8')),
            'wsgi.errors':          sys.stderr,
            'wsgi.multithread':     False,
            'wsgi.multiprocess':    False,
            'wsgi.run_once':        False,
            # Required CGI variables
            'REQUEST_METHOD':       self.request_method,    # GET
            'PATH_INFO':            self.path,              # /hello
            'SERVER_NAME':          self.server_name,       # localhost
            'SERVER_PORT':          str(self.server_port)   # 8888
        }
        return env

    def start_response(self, status, response_headers, exec_info=None):
        # Add necessary server headers
        server_headers = [
            ('Date', 'Monday, 16 July 2018 5:54:32 PST'),
            ('Server', 'WSGIServer 0.2')
        ]
        self.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. For simplicity, ignored for now.
        # return self.finish_response

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data.decode('utf8')
            # Print formatted response data a la 'curl -v'
            print(''.join('> {line}\n'.format(line=line)
                          for line in response.splitlines()))
            response = response.encode()
            self.client_connection.sendall(response)
        finally:
            self.client_connection.close()


SERVER_ADDRESS = (HOST, PORT) = '', 8888


def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    server = make_server(SERVER_ADDRESS, application)
    print('WSGIServer: Serving HTTP on port {port} ...\n'.format(port=PORT))
    server.run()
