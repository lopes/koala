#!/usr/bin/env python3

from base64 import b64encode
from urllib.request import Request, urlopen
from json import loads


class Prime(object):
    def __init__(self, proto, server, endpoint, resource, query, maxresults,
        user, password):
        self.url = f'{proto}://{server}/{endpoint}/{resource}'
        self.query = query
        self.maxresults = int(maxresults)
        self.auth = b64encode(f'{user}:{password}'.encode()).decode()
        self.total = self.get_num_devices()
    
    def get_num_devices(self):
        # Only compatible with JSON resource --Devices.json
        self.req = Request(f'{self.url}?.maxResults=1',
            headers={'Authorization':f'Basic {self.auth}'}, method='GET')
        with urlopen(self.req) as r:
            return int(loads(r.read())['queryResponse']['@count'])

    def get_devices(self):
        devices = list()
        for i in range(0, self.total, self.maxresults):
            req = Request(f'{self.url}?.full=true&.sort=ipAddress&.maxResults={self.maxresults}&.firstResult={i}',
                headers={'Authorization':f'Basic {self.auth}'}, method='GET')
            with urlopen(req) as r:
                for device in loads(r.read())['queryResponse']['entity']:
                    d_address = device['devicesDTO']['ipAddress']
                    try: d_name = device['devicesDTO']['deviceName']
                    except KeyError: d_name = None
                    try: d_type = device['devicesDTO']['deviceType']
                    except KeyError: d_type = None
                    try: d_family = device['devicesDTO']['productFamily']
                    except KeyError: d_family = None
                    try: d_swtype = device['devicesDTO']['softwareType']
                    except KeyError: d_swtype = None
                    try: d_swversion = device['devicesDTO']['softwareVersion']
                    except KeyError: d_swversion = None
                    devices.append({
                        'address': d_address,
                        'name': d_name,
                        'type': d_type,
                        'family': d_family,
                        'software': {'type': d_swtype,'version': d_swversion}})
        return devices