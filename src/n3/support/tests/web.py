from threading import Thread
from unittest import TestCase
from n3.support.cert import create_self_signed_cacert, create_session_cert
from n3.support.web import SecureHTTPServer, SecureHTTPRequestHandler


class TestServer(TestCase):

    def test_server(self):
        cacert, cakey = create_self_signed_cacert()
        cert, key = create_session_cert(cacert, cakey)
        server = SecureHTTPServer(('localhost', 4443), key, cert, SecureHTTPRequestHandler)
        Thread(target=server.serve_forever()).run()
