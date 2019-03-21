#!/usr/bin/env python3

from base64 import b64encode
from urllib.request import Request, urlopen


class Prime(object):
    def __init__(self, proto, server, endpoint, resource, query, 
        user, password):
        self.url = f'{proto}://{server}/{endpoint}/{resource}?{query}'
        self.auth = b64encode(f'{user}:{password}'.encode()).decode()
        self.req = Request(f'{self.url}',
            headers={'Authorization':f'Basic {self.auth}'},
            method='GET')
    
    def get_data(self):
        with urlopen(self.req) as r:
            return r.read().decode()
