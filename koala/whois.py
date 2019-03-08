#!/usr/bin/env python3

from ipaddress import ip_address, ip_network
from requests import get
from os.path import join
from tarfile import open as taropen
from shutil import move, rmtree
from os import unlink
from re import match
from math import log2

from ipwhois import IPWhois
from geoip2.database import Reader


class RDAP(object):
    def __init__(self, addr):
        self.addr = ip_address(addr)
        if self.addr.is_global:
            self.rdap = self.get_rdap_info()
        else:
            raise IOError
    
    def get_rdap_info(self):
        return IPWhois(str(self.addr)).lookup_rdap()
    
    def show_asn(self, rdap):
        properties = {'nir':'NIR', 'asn_registry':'RIR', 'asn':'ASN',
            'asn_cidr':'CIDR', 'asn_country_code':'Country', 
            'asn_date':'Date', 'asn_description':'Description'}
        print('[ASN]')
        for k,v in rdap.items():
            if k in properties:
                print('\t{: <20}{}'.format(properties[k], v))
    
    def show_network(self, rdap):
        properties = {'cidr':'CIDR', 'start_address':'Start address',
            'end_address':'End address', 'status':'Status',
            'name':'Name', 'country':'Country', 'links':'Link',
            'ip_version':'IP version'}
        net = rdap['network']
        print('[NETWORK]')
        for k,v in net.items():
            if k in properties:
                if k == 'status' and v:
                    for i in v:
                        print('\t{: <20}{}'.format('Status', i))
                elif k == 'links':
                    for i in v:
                        print('\t{: <20}{}'.format('Link', i))
                else:
                    print('\t{: <20}{}'.format(properties[k], v))
        
    def show_object(self, rdap):
        properties = {'entities':'Entity', 'links':'Link',
            'contact':'Contact', 'email':'E-mail', 'name':'Name',
            'roles':'Role'}
        obj = rdap['objects']
        for k,v in obj.items():
            print(f'[{k}]')
            for ok,ov in v.items():
                if ok in properties:
                    if (ok == 'entities' or ok == 'links') and ov:
                        for i in ov:
                            print('\t{: <20}{}'.format(properties[ok], i))
                    elif ok == 'contact' and ov:
                        for ook,oov in ov.items():
                            if ook in properties:
                                if ook == 'email' and oov:
                                    for i in oov:
                                        print('\t{: <20}{}'.format(properties[ook], i['value']))
                    elif ok == 'roles' and ov:
                        for i in ov:
                            print('\t{: <20}{}'.format(properties[ok], i))
                    else:
                        print('\t{: <20}{}'.format(properties[ok], ov))
    
    def show(self):
        self.show_asn(self.rdap)
        self.show_network(self.rdap)
        self.show_object(self.rdap)
    
    def raw(self):
        print(self.rdap)


class InstallOffLine(object):
    def __init__(self, path):
        self.path = path
        self.rir_urls = {
            'lacnic': 'http://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest',
            'afrinic': 'https://ftp.ripe.net/pub/stats/afrinic/delegated-afrinic-latest', 
            'apnic': 'https://ftp.apnic.net/stats/apnic/delegated-apnic-latest',
            'arin': 'https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest',
            'ripe': 'https://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-latest'
        }
        self.geo_urls = {
            'city': 'https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz',
            'asn': 'https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN.tar.gz'
        }
    
    def rir(self):
        for r in self.rir_urls:
            print(f'Downloading {r}')
            data = get(self.rir_urls[r])
            with open(join(self.path,r),'wb') as f:
                f.write(data.content)

    def geo(self):
        for g in self.geo_urls:
            n = self.geo_urls[g].split('/')[-1]
            print(f'Downloading {n}')
            data = get(self.geo_urls[g])
            with open(join(self.path,n),'wb') as f:
                f.write(data.content)
            t = taropen(join(self.path, n), 'r')
            for m in t.getmembers():
                if '.mmdb' in m.name:
                    t.extract(m, self.path)
                    move(join(self.path, m.name), join(self.path, m.name.split('/')[-1]))
                    rmtree(join(self.path, m.name.split('/')[0]))
            t.close()
            unlink(join(self.path, n))

    def all(self):
        print(f'Updating local databases: {self.path}')
        self.rir()
        self.geo()


class OffLine(object):
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
                        if self.addr in ip_network(f'{s[3]}/{32-int(log2(int(s[4])))}',
                            False):
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
    
    def show(self):
        rir = self.get_rir_info()
        geo = self.get_geo_info()
        print('[RIR]\n\tName\t\t{}\n\tNetwork\t\t{}\n\tDate\t\t{}\n\tStatus\t\t{}'.format(rir[0], rir[1], rir[2], rir[3]))
        print('[GEO]\n\tASN\t\t{}\n\tOrganization\t{}\n\tAddress\t\t{}, {}\n\tCoordinates\t({}, {})\n\tMap\t\t{}'.format(geo[0], geo[1], geo[2], geo[3], geo[4], geo[5], f'https://www.latlong.net/c/?lat={geo[4]}&long={geo[5]}'))
