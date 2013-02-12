#!/bin/bash

source env/bin/activate
PYTHONPATH=src python src/n3/server.py -d
