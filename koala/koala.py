#!/usr/bin/env python3

from os.path import expanduser, exists, join
from os import makedirs
from argparse import ArgumentParser

from info import Info
from update import Update
from check import Check


local_db_path = join(expanduser('~'), '.koala')

parser = ArgumentParser(description='IP information')
subparser = parser.add_subparsers(help='commands')

update_parser = subparser.add_parser('update',
    help='Updates local databases')
update_parser.add_argument('db', action='store', 
    choices=('rir','geoip2','all'))

info_parser = subparser.add_parser('info',
    help='Shows info about IP network')
info_parser.add_argument('info_ip', action='store', default=None)

check_parser = subparser.add_parser('check',
    help='Checks information about IP addresses')
check_parser.add_argument('check_value', action='store', 
    default=None)

args = parser.parse_args()


if __name__ == '__main__':
    if not exists(local_db_path):
        makedirs(local_db_path)
    
    try:
        Check(local_db_path, args.check_value).show()
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
        Info(args.info_ip).show()
        exit(0)
    except AttributeError:
        pass