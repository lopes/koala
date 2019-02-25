#!/usr/bin/env python3

from ipaddress import ip_address

from ipwhois import IPWhois


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