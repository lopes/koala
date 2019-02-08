#!/usr/bin/env python3

from ipaddress import ip_address, ip_network


class Info(object):
    def __init__(self, addr):
        self.address = ip_address(addr.split('/')[0])
        self.network = ip_network(addr, False)
    
    def show(self):
        print('Address\t\t{}\t{:032b}'.format(self.address, int(self.address)))
        print('Network (/{})\t{}\t{:032b}'.format(self.network.prefixlen, 
            self.network.netmask, int(self.network.netmask)))
        print('Wildcard\t{}\t{:032b}'.format(self.network.hostmask, 
            int(self.network.hostmask)))
        print('Net addr\t{}\t{:032b}'.format(self.network.network_address, 
            int(self.network.network_address)))
        print('Broadcast\t{}\t{:032b}'.format(self.network.broadcast_address, 
            int(self.network.broadcast_address)))
        print('# addresses\t{}'.format(self.network.num_addresses))

        if self.address.is_private:
            print('Private addr')