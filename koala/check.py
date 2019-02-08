#!/usr/bin/env python3

from os.path import join
from ipaddress import ip_address, ip_network
from re import match
from math import log2
from pprint import pprint

from geoip2.database import Reader
from ipwhois import IPWhois


class Check(object):
    def __init__(self, path, addr):
        self.path = path
        self.addr = ip_address(addr)
        self.rirs = ('afrinic', 'apnic', 'arin', 'lacnic', 'ripe')
        self.geo = ('GeoLite2-ASN.mmdb', 'GeoLite2-City.mmdb')
    
    def get_rir_info(self):
        ipline = r'^[a-z]+\|[A-Z]{2}\|ipv[46]\|'
        for r in self.rirs:
            with open(join(self.path,r), 'r') as f:
                for line in f.readlines():
                    if match(ipline, line):
                        s = line.split('|')
                        if self.addr in ip_network(f'{s[3]}/{32-int(log2(int(s[4])))}', False):
                            rir = r.upper()
                            if s[2] == 'ipv4':
                                net = f'{s[3]}/{32-int(log2(int(s[4])))}'
                            else:
                                net = f'{s[3]}/{s[4]}'
                            date = f'{s[5][0:4]}-{s[5][4:6]}-{s[5][6:8]}'
                            status = f'{s[6][:-1]}'
                            return (rir, net, date, status)
        return None
    
    def get_geo_info(self):
        geo_asn = Reader(join(self.path, self.geo[0])).asn(str(self.addr))
        geo_city = Reader(join(self.path, self.geo[1])).city(str(self.addr))
        return (geo_asn.autonomous_system_number,
            geo_asn.autonomous_system_organization,
            geo_city.country.name,
            geo_city.city.name,
            geo_city.location.latitude,
            geo_city.location.longitude)
    
    def get_whois_info(self):
        who = IPWhois(str(self.addr)).lookup_rdap()
        return who
    
    def show(self):
        rir = self.get_rir_info()
        geo = self.get_geo_info()
        who = self.get_whois_info()
        print('[RIR]\n\tName\t{}\n\tNetwork\t{}\n\tDate\t{}\n\tStatus\t{}\n'.format(rir[0], rir[1], rir[2], rir[3]))
        print('[GEO]\n\tASN\t\t{}\n\tOrganization\t{}\n\tCountry\t\t{}\n\tCity\t\t{}\n\tLatitude\t{}\n\tLongitude\t{}\n\tMap\t\t{}\n'.format(geo[0], geo[1], geo[2], geo[3], geo[4], geo[5], f'https://www.latlong.net/c/?lat={geo[4]}&long={geo[5]}'))
        print('[WHOIS]')
        pprint(who)