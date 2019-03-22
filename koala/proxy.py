#!/usr/bin/env python3

'''Sets Windows' proxy configurations easily.

This script allows user to update Windows proxy settings easily,
by using predefined values assigned to proxies identified by
keywords.

Note that it'll also refresh your system to guarantee that all
settings take effect.  Although in the tests it seemed unnecessary
(Windows 8.1), it's considered just a guarantee.

Of course, you must reload all pages after running this script, but
the first thing you gotta do before running it is to setup the PROXIES
variable, creating an ID for each proxy in your environment, so you
can refer to it by using that ID as a parameter.

The "default" and "off" words are reserved, one for your proxy default
settings and the other to disable proxy --remember to set up the 
"default" keyword properly.  Running this script without parameters
will print the current proxy settings on screen.

Based on: https://bitbucket.org/canassa/switch-proxy
'''


import ctypes

from platform import system
from sys import argv
from winreg import OpenKey, QueryValueEx, SetValueEx
from winreg import HKEY_CURRENT_USER, KEY_ALL_ACCESS

from koala import KoalaError


WIN_INTERNET_SETTINGS = OpenKey(HKEY_CURRENT_USER, 
    r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
    0, KEY_ALL_ACCESS)


class Proxy(object):
    def __init__(self, enable=False, server=None, override=None):
        self.os = system()
        self.enable = enable
        self.server = server
        self.override = override

    def win_set_key(self, name, value):
        SetValueEx(WIN_INTERNET_SETTINGS, name, 0, 
            QueryValueEx(WIN_INTERNET_SETTINGS, name)[1], value)
    
    def win_apply(self):
        enable = 1 if self.enable else 0
        self.win_set_key('ProxyEnable', enable)
        if self.enable:
            self.win_set_key('ProxyOverride', self.override)
            self.win_set_key('ProxyServer', self.server)

        # granting the system refresh for settings take effect
        internet_set_option = ctypes.windll.Wininet.InternetSetOptionW
        internet_set_option(0, 37, 0, 0)  # refresh
        internet_set_option(0, 39, 0, 0)  # settings changed
    
    def apply(self):
        if self.os == 'Windows':
            self.win_apply()
        else:
            KoalaError(f'ERROR: unsupported OS: {self.os}')
    
    def show(self):
        if self.os == 'Windows':
            if QueryValueEx(WIN_INTERNET_SETTINGS,"ProxyEnable")[0]:
                print(f'SERVER\n{QueryValueEx(WIN_INTERNET_SETTINGS,"ProxyServer")[0]}')
                print(f'EXCEPTIONS\n{QueryValueEx(WIN_INTERNET_SETTINGS,"ProxyOverride")[0]}')
            else:
                print('Proxy is disabled.')
        else:
            raise KoalaError(f'ERROR: unsupported OS: {self.os}')
