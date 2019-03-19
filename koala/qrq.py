#!/usr/bin/env python3

from sys import argv
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from json import loads
from time import sleep

from koala import KoalaError


'''
Performs queries in IBM QRadar.

Requires a valid token and a QRadar instace (tested
under v7.3.0).  The only query implemented at this
moment is `top5-hp`.

Before start using, you must setup at least TOKEN,
CIDR, and SERVER constants according to your
environment.
'''
__author__ = 'José Lopes'
__license__ = 'MIT'


class QRadarQuery(object):
    def __init__(self, proto, server, path, token, query, retry, sleep):
        self.url = f'{proto}://{server}/{path}'
        self.token = token
        self.query = quote(query)
        self.retry = int(retry)
        self.sleep = int(sleep)
        self.search_id = self.request_search()
        self.results = self.get_results()

    def request_search(self):
        req = Request(f'{self.url}?query_expression={self.query}', 
            headers={'Content-Type':'application/json','SEC':self.token}, 
            method='POST')
        print(f'Requesting search to {self.url}')
        with urlopen(req) as r:
            return loads(r.read())['search_id']

    def get_results(self):
        req = Request(f'{self.url}/{self.search_id}/results', 
            headers={'Content-Type':'application/json','SEC':self.token}, 
            method='GET')
        for t in range(1, self.retry+1):
            print(f'Requesting results ({t}/{self.retry})')
            sleep(self.sleep)
            try:
                with urlopen(req) as r:
                    return loads(r.read())
            except HTTPError:
                pass
        KoalaError(f'Can\'t retrieve results (Search ID: {self.search_id})')
