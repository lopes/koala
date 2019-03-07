#!/usr/bin/env python3

from os.path import expanduser, exists, join
from os import makedirs
from argparse import ArgumentParser
from configparser import ConfigParser

from subnet import Subnet
from rdap import RDAP
from iron import Iron
from proxy import Proxy

from update import Update
from info import Info


conf_file = join(expanduser('~'), '.koala.conf')
local_db_path = join(expanduser('~'), '.koala')

# Argparse
parser = ArgumentParser(description='IP information')
subparser = parser.add_subparsers(help='commands')

subnet_parser = subparser.add_parser('subnet',
    help='IP subnet calculator')
subnet_parser.add_argument('subnet_ip', action='store', default=None)

rdap_parser = subparser.add_parser('rdap',
    help='Retrieves RDAP information from the internet')
rdap_parser.add_argument('rdap_ip', action='store', default=None)

iron_parser = subparser.add_parser('iron',
    help='IronPort domain list clean-up')
iron_parser.add_argument('iron_file', action='store', default=None)

proxy_parser = subparser.add_parser('proxy',
    help='Proxy settings')
proxy_parser.add_argument('proxy_id', action='store', default=None)

visio_parser = subparser.add_parser('visio',
    help='Exports MS-Visio files to PDF in batch')
# visio_parser.add_argument('visio', action='store', default=None)

args = parser.parse_args()

conf = ConfigParser()
conf.read(conf_file)


if __name__ == '__main__':
    if hasattr(args, 'subnet_ip'):
        Subnet(args.subnet_ip).show()
    elif hasattr(args, 'rdap_ip'):
        RDAP(args.rdap_ip).show()
    elif hasattr(args, 'iron_file'):
        Iron(args.iron_file).show()
        
    elif hasattr(args, 'proxy_id'):
        try:
            if args.proxy_id == 'status':
                Proxy().show()
            else:
                if args.proxy_id != 'off':
                    proxy_enable = True
                    proxy_server = conf['PROXY'][args.proxy_id]
                    proxy_override = conf['DEFAULT']['proxy_override']
                    proxy = Proxy(proxy_enable, proxy_server, proxy_override)
                else:
                    proxy = Proxy()
                proxy.apply()
                proxy.show()
        except KeyError:
            print(f'Error: unknown proxy id {args.proxy_id}\nTip: ', end='')
            values = [v[0] for v in conf.items('PROXY')]
            values.remove('proxy_override')
            print(values, '\nOr use \'off\' to disable proxy.')

    exit(0)
