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


from os import access, walk, R_OK, W_OK, remove
from os.path import abspath, join
from re import compile, match, sub, IGNORECASE
from shutil import rmtree

from koala import KoalaError

try:
    import win32com.client
except ModuleNotFoundError:
    raise KoalaError('module win32com not found')


class Visio(object):
    def __init__(self, format, erase, source, destination):
        self.format = 'pdf' if format else 'html'
        self.erase = True if erase else False
        self.source = abspath(source)
        self.destination = abspath(destination)
        self.is_vsd = compile(r'^.*\.vsd$', IGNORECASE)

        # win32com doesn't throw exceptions properly, so 
        # must perform these checks.  sorry, duck typing!
        if not access(self.source, R_OK):
            KoalaError(f'not readable: {self.source}')
        if not access(self.destination, W_OK):
            KoalaError(f'not writable: {self.destination}')

    def vsd2pdf(self, vsd, pdf):
        visio = win32com.client.Dispatch('Visio.InvisibleApp')
        visio.Documents.Open(vsd).ExportAsFixedFormat(
            1, f'{pdf}.pdf', 0, 0)
        visio.Quit()

    def vsd2web(self, vsd, html):
        '''Thanks to Nikolay Belykh: github.com/nbelyh'''
        visio = win32com.client.Dispatch('Visio.InvisibleApp')
        doc = visio.Documents.Open(vsd)
        visio.Addons('SaveAsWeb').Run(f'/quiet /target={html}.html')
        visio.Quit()
    
    def apply(self):
        if self.erase:
            for root, dirs, files in walk(self.destination):
                for f in files:
                    print(f'INFO: deleting {f}')
                    try:
                        remove(join(root, f))
                    except PermissionError:
                        print(f'ERROR: already opened? {f}')
                for d in dirs:
                    print(f'INFO: deleting {d}')
                    try:
                        rmtree(join(root, d))
                    except PermissionError:
                        print(f'ERROR: already opened? {f}')
            
        for root, dirs, files in walk(self.source):
            for f in files:
                if match(self.is_vsd, f):
                    print(f'INFO: processing {f}')
                    try:
                        if self.format == 'pdf':
                            self.vsd2pdf(join(root, f), 
                                join(self.destination, sub(r'\.vsd$','',f)))
                        elif self.format == 'html':
                            self.vsd2web(join(root, f), 
                                join(self.destination, sub(r'\.vsd$','',f)))
                    except Exception:  # win32com is generic
                        print(f'ERROR: already opened? {f}');print('foo')
                else:
                    print(f'INFO: skipped {f}')
