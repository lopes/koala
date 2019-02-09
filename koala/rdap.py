#!/usr/bin/env python3

from ipaddress import ip_address
from pprint import pprint

from ipwhois import IPWhois


class RDAP(object):
    def __init__(self, addr):
        self.addr = ip_address(addr)
    
    def get_rdap_info(self):
        return IPWhois(str(self.addr)).lookup_rdap()
    
    def show(self):
        print('[RDAP]')
        pprint(self.get_rdap_info())