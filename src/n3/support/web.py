
from os.path import join
from http.server import HTTPServer, SimpleHTTPRequestHandler
from ssl import SSLContext, PROTOCOL_TLSv1


class SecureHTTPServer(HTTPServer):

    def __init__(self, server_address, HandlerClass, dir):
        super().__init__(server_address, HandlerClass, bind_and_activate=False)
        ctx = SSLContext(PROTOCOL_TLSv1)
        ctx.load_cert_chain(join(dir, 'server-cert.pem'), join(dir, 'server-key.pem'))
#        ctx.load_verify_locations(join(dir, 'ca-cert.pem'))
        self.socket = ctx.wrap_socket(self.socket, server_side=True)
        self.server_bind()
        self.server_activate()

