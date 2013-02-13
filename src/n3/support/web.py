
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socket import socket, _fileobject
from socketserver import BaseServer

from OpenSSL.SSL import Context, SSLv3_METHOD, Connection


class SecureHTTPServer(HTTPServer):

    def __init__(self, server_address, key, cert, HandlerClass):
        # call BaseServer directly to avoid socket creation
        BaseServer.__init__(self, server_address, HandlerClass)
        ctx = Context(SSLv3_METHOD)
        ctx.use_privatekey(key)
        ctx.use_certificate(cert)
        self.socket = Connection(ctx, socket(self.address_family, self.socket_type))
        self.server_bind()
        self.server_activate()


class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):

    def setup(self):
        # set needed attributes in StreamRequestHandler
        self.connection = self.request
        self.rfile = _fileobject(self.request, "rb", self.rbufsize)
        self.wfile = _fileobject(self.request, "wb", self.wbufsize)

