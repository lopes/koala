#!/usr/bin/env python3

from pynetbox import api


class NetBox(object):
    def __init__(self, proto, server, token, tag, unknown):
        self.netbox = api(f'{proto}://{server}', token=token, ssl_verify=False)
        self.tag = tag
        self.unknown = unknown

    def prime_sync(self, devices):
        total = len(devices)
        count = 1
        for device in devices:
            print('[{: >4}/{: >4}] {}:'.format(count,total,device['address']), end=' ')
            try:
                nb = self.netbox.ipam.ip_addresses.get(address=device['address'])
            except ValueError:
                print('duplicated')
                count += 1
                continue
            if nb:
                action = False
                if device['name'] and (nb.description != device['name']):
                    nb.description = device['name']
                    action = True
                if self.tag not in nb.tags:
                    nb.tags.append(self.tag)
                    action = True
                if action:
                    nb.save()
                    print('device updated')
                else:
                    print('nothing to be done')
            else:
                name = device['name'] if device['name'] else self.unknown
                self.netbox.ipam.ip_addresses.create(address=device['address'],
                    description=name, tags=[self.tag])
                print(f'device created')
            count += 1
