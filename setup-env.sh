#!/bin/bash

rm -fr env
virtualenv --python=/usr/local/bin/python3.2 env
source env/bin/activate
easy_install rdflib
easy_install pycrypto
easy_install simple-crypt
easy_install pyopenssl
