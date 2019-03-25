#!/usr/bin/env python3

from base64 import b64encode
from urllib.request import Request, urlopen
from json import loads


class Prime(object):
    def __init__(self, proto, server, endpoint, query, maxresults,
        user, password):
        self.url = f'{proto}://{server}/{endpoint}'
        self.query = query
        self.maxresults = int(maxresults)
        self.auth = b64encode(f'{user}:{password}'.encode()).decode()
        self.total_devices = self.get_num_devices()
        self.total_aps = self.get_num_aps()
    
    def get_num_devices(self):
        # Only compatible with JSON resource --Devices.json
        self.req = Request(f'{self.url}/Devices.json?.maxResults=1',
            headers={'Authorization':f'Basic {self.auth}'}, method='GET')
        with urlopen(self.req) as r:
            return int(loads(r.read())['queryResponse']['@count'])
    
    def get_num_aps(self):
        # Only compatible with JSON resource --AccessPoints.json
        self.req = Request(f'{self.url}/AccessPoints.json?.maxResults=1',
            headers={'Authorization':f'Basic {self.auth}'}, method='GET')
        with urlopen(self.req) as r:
            return int(loads(r.read())['queryResponse']['@count'])

    def get_devices(self):
        devices = list()
        for i in range(0, self.total_devices, self.maxresults):
            req = Request(f'{self.url}/Devices.json?.full=true&.sort=ipAddress&.maxResults={self.maxresults}&.firstResult={i}',
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
                    try: d_location = device['devicesDTO']['location']
                    except KeyError: d_location = None
                    devices.append({
                        'address': d_address,
                        'name': d_name,
                        'info': {'type': d_type, 'family': d_family,
                            'location': d_location,
                            'software': {
                                'type': d_swtype,'version': d_swversion
                        }}})
                    #TODO: get more info from device
        return devices

    def get_aps(self):
        aps = list()
        for i in range(0, self.total_aps, self.maxresults):
            req = Request(f'{self.url}/AccessPoints.json?.full=true&.sort=ipAddress&.maxResults={self.maxresults}&.firstResult={i}',
                headers={'Authorization':f'Basic {self.auth}'}, method='GET')
            with urlopen(req) as r:
                for ap in loads(r.read())['queryResponse']['entity']:
                    ap_address = ap['accessPointsDTO']['ipAddress']['address']
                    try: ap_name = ap['accessPointsDTO']['name']
                    except KeyError: ap_name = None
                    try: ap_location = ap['accessPointsDTO']['location']
                    except KeyError: ap_location = None
                    try: ap_serial = ap['accessPointsDTO']['serialNumber']
                    except KeyError: ap_serial = None
                    try: ap_swversion = ap['accessPointsDTO']['softwareVersion']
                    except KeyError: ap_swversion = None
                    try: ap_primeid = ap['accessPointsDTO']['@id']
                    except KeyError: ap_primeid = None
                    aps.append({
                        'address': ap_address,
                        'name': ap_name,
                        'info': {
                            'location': ap_location,
                            'serial': ap_serial,
                            'software_version': ap_swversion,
                            'prime_id': ap_primeid,
                            'location': ap_location
                        }})
        return aps
