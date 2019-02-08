#!/usr/bin/env python3


from requests import get
from os.path import join
from tarfile import open as taropen
from shutil import move, rmtree
from os import unlink


class Update(object):
    def __init__(self, path):
        self.path = path
        self.rir_urls = {
            'lacnic': 'http://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest',
            'afrinic': 'https://ftp.ripe.net/pub/stats/afrinic/delegated-afrinic-latest', 
            'apnic': 'https://ftp.apnic.net/stats/apnic/delegated-apnic-latest',
            'arin': 'https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest',
            'ripe': 'https://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-latest'
        }
        self.geolite2_urls = {
            'city': 'https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz',
            'asn': 'https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN.tar.gz'
        }
    
    def rir(self):
        for r in self.rir_urls:
            data = get(self.rir_urls[r])
            with open(join(self.path,r),'wb') as f:
                f.write(data.content)

    def geoip2(self):
        for g in self.geolite2_urls:
            n = self.geolite2_urls[g].split('/')[-1]
            data = get(self.geolite2_urls[g])
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
        self.rir()
        self.geoip2()