#!/usr/bin/env python3

from koala import args, conf, KoalaError
from koala.subnet import Subnet
from koala.whois import RDAP
from koala.iron import Iron
from koala.proxy import Proxy
from koala.visio import Visio
from koala.qrq import QRadarQuery
from koala.abuse import Abuse


if __name__ == '__main__':
    try:
        if args.command == 'subnet':
            Subnet(args.cidr).show()
        elif args.command == 'whois':
            RDAP(args.ip).show()
        elif args.command == 'iron':
            Iron(args.iron_file).show()
        elif args.command == 'visio':
            c = conf['VISIO']
            Visio(c['format'], c['erase'], c['source'], c['destination']).apply()
        elif args.command == 'qrq':
            c = conf['QRQ']
            qrq = QRadarQuery(c['proto'], c['server'], c['path'], c['token'], 
                c[args.qrquery], c['retry'], c['sleep'])
            print(qrq.results)
        elif args.command == 'abuse':
            abuse = Abuse(conf['ABUSE']['server'], conf['ABUSE']['user'],
                conf['ABUSE']['password'], conf['ABUSE']['workbox'], 
                conf['ABUSE']['bkpbox'])
        elif args.command == 'proxy':
            try:
                if args.id == 'status':
                    Proxy().show()
                else:
                    if args.id != 'off':
                        proxy_enable = True
                        proxy_server = conf['PROXY'][args.id]
                        proxy_override = conf['PROXY_OVERRIDE']['addresses'] if args.id != 'burp' else '-'
                        proxy = Proxy(proxy_enable, proxy_server, proxy_override)
                    else:
                        proxy = Proxy()
                    proxy.apply()
                    proxy.show()
            except KeyError:
                print(f'ERROR: unknown proxy id {args.id}\nTIP: ', end='')
                values = [v[0] for v in conf.items('PROXY')]
                print(values, '\nOr use \'off\' to disable proxy.')
    except KoalaError as ke:
        print(f'ERROR: {ke}')
        exit(1)
    exit(0)
