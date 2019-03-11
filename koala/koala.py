#!/usr/bin/env python3

from os.path import expanduser, exists, join
from os import makedirs
from argparse import ArgumentParser
from configparser import ConfigParser

from subnet import Subnet
from whois import RDAP
from iron import Iron
from proxy import Proxy
from visio import Visio
from qrq import QRadarQuery
from abuse import Abuse


conf_file = join(expanduser('~'), '.koala.conf')
local_db_path = join(expanduser('~'), '.koala')

parser = ArgumentParser(description='CORS\'s Swiss Army Knife')
subparser = parser.add_subparsers(help='commands')

subnet_parser = subparser.add_parser('subnet',
    help='IP subnet calculator')
subnet_parser.add_argument('subnet_ip', action='store', default=None)

rdap_parser = subparser.add_parser('whois',
    help='Retrieves whois information from the internet')
rdap_parser.add_argument('whois_ip', action='store', default=None)

iron_parser = subparser.add_parser('iron',
    help='IronPort domain list clean-up')
iron_parser.add_argument('iron_file', action='store', default=None)

proxy_parser = subparser.add_parser('proxy',
    help='Proxy settings')
proxy_parser.add_argument('proxy_id', action='store', default=None)

visio_parser = subparser.add_parser('visio',
    help='Exports MS-Visio files to PDF in batch')
visio_parser.add_argument('visio', action='store_true', default=False)

qrq_parser = subparser.add_parser('qrq',
    help='Performs pre-defined AQL queries in IBM QRadar')
qrq_parser.add_argument('qrquery', action='store', default=None)

abuse_parser = subparser.add_parser('abuse',
    help='Analyses messages sent to abuse boxes')
abuse_parser.add_argument('abuse', action='store_true', default=None)

args = parser.parse_args()
conf = ConfigParser()
conf.read(conf_file)


if __name__ == '__main__':
    if hasattr(args, 'subnet_ip'):
        Subnet(args.subnet_ip).show()
    elif hasattr(args, 'whois_ip'):
        RDAP(args.whois_ip).show()
    elif hasattr(args, 'iron_file'):
        Iron(args.iron_file).show()
    elif hasattr(args, 'visio'):
        Visio(conf['VISIO']['format'], conf['VISIO']['erase'],
            conf['VISIO']['source'], conf['VISIO']['destination']).apply()
    elif hasattr(args, 'qrquery'):
        qrq = QRadarQuery(conf['QRQ']['proto'], conf['QRQ']['server'], 
            conf['QRQ']['path'], conf['QRQ']['token'], 
            conf['QRQ'][args.qrquery], conf['QRQ']['retry'], 
            conf['QRQ']['sleep'])
        print(qrq.results)
    elif hasattr(args, 'abuse'):
        abuse = Abuse(conf['ABUSE']['server'], conf['ABUSE']['user'],
            conf['ABUSE']['password'], conf['ABUSE']['workbox'], 
            conf['ABUSE']['bkpbox'])
    elif hasattr(args, 'proxy_id'):
        try:
            if args.proxy_id == 'status':
                Proxy().show()
            else:
                if args.proxy_id != 'off':
                    proxy_enable = True
                    proxy_server = conf['PROXY'][args.proxy_id]
                    proxy_override = conf['PROXY_OVERRIDE']['addresses']
                    proxy = Proxy(proxy_enable, proxy_server, proxy_override)
                else:
                    proxy = Proxy()
                proxy.apply()
                proxy.show()
        except KeyError:
            print(f'ERROR: unknown proxy id {args.proxy_id}\nTIP: ', end='')
            values = [v[0] for v in conf.items('PROXY')]
            print(values, '\nOr use \'off\' to disable proxy.')
    exit(0)
