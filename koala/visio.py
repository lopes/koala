#!/usr/bin/env python3
#vsdbatch.py


'''
vsdbatch
Exports multiple Visio files in batch.

REQUIREMENTS
    1. Python 3.6  -- and pip3
    2. Pywin32  -- pip install pywin32
    3. Visio 2013

INSTALLATION
Having all requirements satisfied, just copy this
script to your machine and run it.
'''
__author__ = 'José Lopes de Oliveira Jr.'
__copyright__ = 'Copyright 2018, Cemig'
__license__ = 'MIT'
__version__ = '0.11.2'


import win32com.client

from argparse import ArgumentParser
from logging import basicConfig, DEBUG, info, error
from os import access, walk, R_OK, W_OK, remove
from os.path import abspath, join
from re import compile, match, sub, IGNORECASE
from sys import stdout
from shutil import rmtree


basicConfig(stream=stdout, level=DEBUG,
    format='%(asctime)s %(name)s %(levelname)s %(message)s')

argp = ArgumentParser()
argp.add_argument('-f', '--format', help='creates PDF or HTML files', 
    choices=['pdf', 'html'])
argp.add_argument('-e', '--erase', help='erases destination directory', 
    action='store_true')
argp.add_argument('source', help='Visio files repository path')
argp.add_argument('destination', help='new files directory path')
args = argp.parse_args()

source = abspath(args.source)
destination = abspath(args.destination)
isvsd = compile(r'^.*\.vsd$', IGNORECASE)

# win32com doesn't throw exceptions properly, so 
# must perform these checks.  sorry, duck typing!
if not access(args.source, R_OK):
    print('Error: not readable: {}'.format(source))
    exit(1)
if not access(args.destination, W_OK):
    print('Error: not writable: {}'.format(destination))
    exit(1)


def vsd2pdf(s, t):
    '''Converts a VSD file to PDF.
    Args:
        - (s)ource (string): path to VSD file
        - (t)arget (string): path to PDF (output) file
    '''
    visio = win32com.client.Dispatch("Visio.InvisibleApp")
    visio.Documents.Open(s).ExportAsFixedFormat(1, '{}.pdf'.format(t), 0, 0)
    visio.Quit()

def vsd2web(s, t):
    '''Converts a VSD file to HTML.
    Args:
        - (s)ource (string): path to VSD file
        - (t)arget (string): path to HTML (output) file
    Note:
    Thanks to Nikolay Belykh (github.com/nbelyh).
    '''
    visio = win32com.client.Dispatch('Visio.InvisibleApp')
    doc = visio.Documents.Open(s)
    visio.Addons('SaveAsWeb').Run('/quiet /target={}.html'.format(t))
    visio.Quit()


if args.erase:
    for root, dirs, files in walk(destination):
        for f in files:
            info('deleting {}'.format(f))
            try:
                remove(join(root, f))
            except PermissionError:
                error('already opened?: {}'.format(f))
        for d in dirs:
            info('deleting {}'.format(d))
            try:
                rmtree(join(root, d))
            except PermissionError:
                error('already opened?: {}'.format(f))
    
for root, dirs, files in walk(source):
    for f in files:
        if match(isvsd, f):
            info('processing {}'.format(f))
            try:
                if args.format == 'pdf':
                    vsd2pdf(join(root,f),
                        join(destination,sub(r'\.vsd$','',f)))
                elif args.format == 'html':
                    vsd2web(join(root,f),
                        join(destination,sub(r'\.vsd$','',f)))
                else:
                    print('Error: unknown output: {}'.format(output))
                    exit(1)
            except Exception:  # win32com is generic
                error('already opened?: {}'.format(f))
        else:
            info('skipped {}'.format(f))

exit(0)