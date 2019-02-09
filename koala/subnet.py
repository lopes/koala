#!/usr/bin/env python3

from ipaddress import ip_address, ip_network


class Subnet(object):
    def __init__(self, addr):
        self.address = ip_address(addr.split('/')[0])
        self.network = ip_network(addr, False)
    
    def show(self):
        print('Address\t\t{: <20} {:032b}'.format(str(self.address), int(self.address)))
        print('Mask (/{})\t{: <20} {:032b}'.format(self.network.prefixlen, 
            str(self.network.netmask), int(self.network.netmask)))
        print('Wildcard\t{: <20} {:032b}'.format(str(self.network.hostmask), 
            int(self.network.hostmask)))
        print('Netaddr\t\t{: <20} {:032b}'.format(str(self.network.network_address), 
            int(self.network.network_address)))
        print('Broadcast\t{: <20} {:032b}'.format(str(self.network.broadcast_address), 
            int(self.network.broadcast_address)))
        print('# addresses\t{}'.format(self.network.num_addresses))
        print('Reverse pointer\t{}'.format(self.address.reverse_pointer))

        if self.address.is_private:
            print('Private addr')