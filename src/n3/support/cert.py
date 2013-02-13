
from logging import getLogger
from os import chmod
from os.path import join, expanduser

from OpenSSL.crypto import PKey, TYPE_RSA, X509, X509Extension, \
    dump_certificate, FILETYPE_PEM, dump_privatekey


LOG = getLogger(__name__)


def create_self_signed_cacert():
    LOG.debug('Creating CA certificate')
    cakey = PKey()
    cakey.generate_key(TYPE_RSA, 1024)
    cacert = X509()
    cacert.get_subject().CN = 'n3'
    cacert.set_serial_number(1)
    cacert.gmtime_adj_notBefore(0)
    cacert.gmtime_adj_notAfter(365*24*60*60)
    cacert.set_issuer(cacert.get_subject())
    cacert.set_pubkey(cakey)
    cacert.add_extensions([
            X509Extension(b'basicConstraints', True, b'CA:TRUE, pathlen:0'),
            X509Extension(b'keyUsage', True, b'keyCertSign, cRLSign'),
            X509Extension(b'subjectKeyIdentifier', False, b'hash', subject=cacert)])
    cacert.sign(cakey, 'sha1')
    return cacert, cakey

def create_session_cert(cacert, cakey, cn='localhost', serial=1):
    LOG.debug('Creating session certificate')
    key = PKey()
    key.generate_key(TYPE_RSA, 1024)
    cert = X509()
    cert.get_subject().CN = cn
    cert.set_serial_number(serial)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)
    cert.set_issuer(cacert.get_subject())
    cert.set_pubkey(key)
    cert.sign(cakey, 'sha1')
    return cert, key

def write_cert(cert, dir, name):
    path = join(expanduser(dir), name)
    LOG.debug('Writing certificate to {}'.format(path))
    with open(path, 'w') as output:
        print(dump_certificate(FILETYPE_PEM, cert).decode('utf8'), end='', file=output)
    chmod(path, 0o600)

def write_key(key, dir, name):
    path = join(expanduser(dir), name)
    LOG.debug('Writing key to {}'.format(path))
    with open(path, 'w') as output:
        print(dump_privatekey(FILETYPE_PEM, key).decode('utf8'), end='', file=output)
    chmod(path, 0o600)
