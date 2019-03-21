from os.path import expanduser, exists, join
from argparse import ArgumentParser
from configparser import ConfigParser


class KoalaError(Exception):
    pass


conf_file = join(expanduser('~'), '.koala.conf')
local_db_path = join(expanduser('~'), '.koala')

parser = ArgumentParser(description='CORS\'s Swiss Army Knife')
subparsers = parser.add_subparsers(title='Commands', dest='command')
subparsers.required = True

argsp = subparsers.add_parser('subnet', help='IP subnet calculator')
argsp.add_argument('cidr', help='An IP in CIDR notation')

argsp = subparsers.add_parser('whois', help='Retrieves whois information from the internet')
argsp.add_argument('ip', help='Target IP')

argsp = subparsers.add_parser('proxy', help='Change proxy settings')
argsp.add_argument('id', help='Proxy ID as configured in .koala.conf')

argsp = subparsers.add_parser('iron', help='Cisco IronPort domain list clean-up')
argsp.add_argument('-i', '--input', required=True, help='Input file with domains')
argsp.add_argument('-o', '--output', required=True, help='Output file')

argsp = subparsers.add_parser('visio', help='Exports multiple MS-Visio files to PDF')

argsp = subparsers.add_parser('qradar', help='Performs pre-defined AQL queries in IBM QRadar')
argsp.add_argument('id', help='AQL ID as configured in .koala.conf')

argsp = subparsers.add_parser('prime', help='Performs pre-defined Cisco Prime queries')

args = parser.parse_args()

conf = ConfigParser()
conf.read(conf_file)
