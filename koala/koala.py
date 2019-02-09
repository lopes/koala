#!/usr/bin/env python3

from os.path import expanduser, exists, join
from os import makedirs
from argparse import ArgumentParser

from subnet import Subnet
from update import Update
from info import Info
from rdap import RDAP


local_db_path = join(expanduser('~'), '.koala')

parser = ArgumentParser(description='IP information')
subparser = parser.add_subparsers(help='commands')

update_parser = subparser.add_parser('update',
    help='Updates local databases')
update_parser.add_argument('db', action='store', choices=('rir','geo','all'))

subnet_parser = subparser.add_parser('subnet',
    help='IP subnet information')
subnet_parser.add_argument('subnet', action='store', default=None)

info_parser = subparser.add_parser('info',
    help='Checks local information about IP addresses')
info_parser.add_argument('info', action='store', default=None)

rdap_parser = subparser.add_parser('rdap',
    help='Retrieves RDAP information from the internet')
rdap_parser.add_argument('rdap', action='store', default=None)

args = parser.parse_args()


if __name__ == '__main__':
    if not exists(local_db_path):
        makedirs(local_db_path)
    
    try:
        Info(local_db_path, args.info).show()
        exit(0)
    except AttributeError:
        pass

    try:
        if args.db == 'all':
            Update(local_db_path).all()
        elif args.db == 'rir':
            Update(local_db_path).rir()
        elif args.db == 'geoip2':
            Update(local_db_path).geoip2()
        exit(0)
    except AttributeError:
        pass

    try:
        Subnet(args.subnet).show()
        exit(0)
    except AttributeError:
        pass
    
    try:
        RDAP(args.rdap).show()
    except AttributeError:
        pass