#!/usr/bin/env python3

'''IronPort Cleaner

This script receives a file with a list of domains from IronPort and
outputs a new list without duplicates (IronPort usually does it
automatically), shadows (.domain.com and domain.com <-removes this),
and overlaps (.domain.com, sub.domain.com <-removes this).

IronCleaner can also check is domains are responsive, but of course
this can be tricky, because of false positives.

Example:
$ ironcleaner.py -i iron-passthrough.txt > new-iron-passthrough.txt
$ ironcleaner.py -c -i iron-whitelist.txt
'''
__author__ = 'José Lopes de Oliveira Júnior'
__license__ = 'MIT'


from re import match


class Iron(object):
    def __init__(self, file_domains, ):
        with open(file_domains, 'r') as f:
            self.domains = sorted(f.readlines()[0].split(', '))
        self.stats = {
            'initial': len(self.domains), 
            'duplicate': 0, 
            'shadowed': 0, 
            'overlapped': 0, 
            'unresponsive': 0
        }
        self.drop_duplicates()
        self.drop_shadows()
        self.drop_overlaps()

    def drop_duplicates(self):
        domains = self.domains.copy()
        for domain in self.domains:
            while domains.count(domain) > 1:
                domains.remove(domain)
                self.stats['duplicate'] += 1
        self.domains = domains

    def drop_shadows(self):
        '''Excludes shadowed domains (.domain.com and domain.com <-this).'''
        domains = self.domains.copy()
        for domain in self.domains:
            if domain.startswith('.'):
                while domains.count(domain[1:]):
                    domains.remove(domain[1:])
                    self.stats['shadowed'] += 1
        self.domains = domains

    def drop_overlaps(self):
        '''Excludes overlaps (.domain.com and sub.domain.com <-this).'''
        domains = self.domains.copy()
        super_domains = [s[1:] for s in domains if s.startswith('.')]
        for domain in self.domains:
            for super_domain in super_domains:
                if match(f'^.+?\.{super_domain}', domain):
                    try:
                        domains.remove(domain)
                        self.stats['overlapped'] += 1
                    except ValueError:
                        pass
        self.domains = domains
    
    def show(self):
        '''Exports the domain list in IronPort format.'''
        print(', '.join(self.domains))
        print(f'\n\nInitial: {self.stats["initial"]}, \
Duplicate: {self.stats["duplicate"]}, Shadowed: {self.stats["shadowed"]}, \
Overlapped: {self.stats["overlapped"]}, \
Unresponsive: {self.stats["unresponsive"]}, Now: {len(self.domains)}')
