
from argparse import ArgumentParser
from logging import getLogger
from socketserver import BaseRequestHandler, TCPServer
from n3.support.cert import create_self_signed_cacert, create_session_cert, \
    write_session_cert, write_session_key, write_cert, write_key

from rdflib import Graph

from n3.support.io import check_config, set_logging, read_encrypted_file


LOG = getLogger(__name__)


def start():
    parser = make_parser()
    args = parser.parse_args()
    set_logging(args.debug, args.verbose)
    check_config(args.config)
    create_certs(args.config)
    data, password = read_encrypted_file(args.file)
    save = lambda x: write_file(args.file, password, x)
    graph = Graph()
    graph.parse(data=data, format='n3')
    start_server(args.bind, args.port, args.config)

def create_certs(dir):
    cacert, cakey = create_self_signed_cacert()
    write_cert(cacert, dir, 'ca-cert.pem')
#    write_key(cakey, dir, 'ca-key.pem')
    cert, key = create_session_cert(cacert, cakey)
    write_cert(cert, dir, 'client-cert.pem')
    write_key(key, dir, 'client-key.pem')
    cert, key = create_session_cert(cacert, cakey)
    write_cert(cert, dir, 'server-cert.pem')
    write_key(key, dir, 'server-key.pem')

def write_file(path, password, data):
    return

def start_server(bind, port, dir):

    class N3Handler(BaseRequestHandler):

        def handle(self):
            self.data = self.request.recv(1024).strip()
            print("{} wrote:".format(self.client_address[0]))
            print(self.data)
            self.request.sendall(self.data.upper())

    server = TCPServer((bind, port), N3Handler)
    server.serve_forever()

def make_parser():
    parser = ArgumentParser(description='Start a server that processes n3 data')
    parser.add_argument('-v', '--verbose', help='verbose output', action='store_true')
    parser.add_argument('-d', '--debug', help='very verbose output', action='store_true')
    parser.add_argument('-b', '--bind', default='localhost', help='bind address for server', metavar='ADDRESS')
    parser.add_argument('-p', '--port', default=14672, type=int, help='port for server', metavar='PORT')
    parser.add_argument('-c', '--config', default='~/.n3', help='configuration directory', metavar='DIR')
    parser.add_argument('-f', '--file', default='~/.n3/n3db', help='knowledge database', metavar='FILE')
    parser.add_argument('-s', '--sleep', default=3600, type=int, help='sleep period before closing', metavar='SECONDS')
    parser.add_argument('-w', '--write', default=10, type=int, help='max wait before writing a copy', metavar='SECONDS')
    return parser


if __name__ == '__main__':
    start()
