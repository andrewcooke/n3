
from getpass import getpass
from logging import getLogger, WARNING, INFO, DEBUG, basicConfig
from os import mkdir, stat, unlink
from os.path import expanduser, exists, isdir

from simplecrypt import decrypt, DecryptionException


LOG = getLogger(__name__)


def check_config(config):
    config = expanduser(config)
    LOG.debug('Checking config at {}'.format(config))
    if not exists(config):
        LOG.info('Creating config at {}'.format(config))
        mkdir(config, 0o700)
    if not isdir(config):
        LOG.error('Config directory {} is not a directory'.format(config))
        exit(1)
    if not stat(config).st_mode == 0o40700:
        LOG.error('Config directory {} has incorrect permissions {}'.format(config, stat(config).st_mode))
        LOG.info('On unix try\n  chmod 0700 {0}'.format(config))
        exit(1)

def read_encrypted_file(path):
    path = expanduser(path)
    password = getpass("password: ")
    if not password: LOG.warn('Empty password - data file unencrypted')
    if not exists(path):
        assert_write_possible(path)
        LOG.info('Will start new data file at ' + path)
        return '', password
    with open(path) as input:
        LOG.info('Trying to read ' + path)
        data = input.read()
        while True:
            try:
                if password: data = decrypt(password, data)
                return data, password
            except DecryptionException:
                LOG.error('Failed to decrypt ' + path)
                password = getpass("password: ")

def assert_write_possible(path):
    LOG.debug('Checking whether we can write to ' + path)
    try:
        with open(path, 'w') as output:
            try:
                output.write('test')
            except:
                raise IOError('Cannot write to ' + path)
    finally:
        if exists(path): unlink(path)

def set_logging(debug, verbose):
    level = WARNING
    if verbose: level = INFO
    if debug: level = DEBUG
    basicConfig(level=level)

