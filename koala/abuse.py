#!/usr/bin/env python3

'''
An abuse mailbox manager.  This program is able to manage an 
abuse mailbox using Internet Message Access Protocol (IMAP).

Abused was implemented at Cemig to be used in the company's 
Network and Security Operations Center (NSOC).  There, we had 
an mailbox (abuse (at) cemig.com.br) which users used to 
notify suspicous email messages.  Everyday, a security analyst 
had to manually process all messages received by this mailbox, 
analyse their headers, and blacklist spammers in the antispam 
tool.

Abused was written to automate this job, by parsing all 
internal messages (*@cemig.com.br).  Abused's main goal was to 
parse crucial data to treat SPAM (i.e., email headers), such as 
the person who notified SPAM, the spoofed address, and the 
servers where the message was relayed.

The first thing is to configure your abuse box with 2 IMAP 
folders: one to redirect all internal (or similar messages) 
and another where processed messages will be stored --in case 
you have to access original files.

WARNING: The password to access the IMAP account will be asked 
and written into the configuration file.  I've found no way to 
guarantee the security of this password, but changing the 
permissions of this file to something more restrictive.

You must setup the mailbox before this running this script, 
inserting the folders ((WORK|BKP)BOX) accordingly.  If some of 
them are misconfigured, then Abused will break with some kind 
of imaplib.error.
'''


import re

from imaplib import IMAP4_SSL
from email import message_from_bytes
from email.header import decode_header


RE_DOMAIN = r'[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
RE_EMAIL = r'[a-zA-Z0-9_.+-]+@{}'.format(RE_DOMAIN)
RE_IPV4 = r'((2([0-4][0-9]|5[0-5])|1?[0-9]?[0-9])\.){3}(2([0-4][0-9]|5[0-5])|1?[0-9]?[0-9])\/(3[012]|[12]?[0-9])'
RE_IPV4_PRIVATE = r'(127\.|10\.|172\.1[6-9]\.|172\.2[0-9]\.|172\.3[0-1]\.|192\.168\.)'
RE_DOMAIN_SELF = r'^(.+\.)?cemig\.(ad\.corp|com\.br)'


class Imap(object):
    def __init__(self, server, user, password, workbox, bkpbox):
        self.server = IMAP4_SSL(server)
        self.server.login(user, password)
        self.workbox = workbox
        self.bkpbox = bkpbox


class Abuse(object):
    def __init__(self, imap_server, imap_user, imap_password, 
        imap_workbox, imap_bkpbox):
        self.imap = Imap(imap_server, imap_user, imap_password, imap_workbox,
            imap_bkpbox)
        self.imap.server.select(imap_workbox)
    
    def get_notifier_addr(self, mail):
        re_notifier = re.compile(r'{}'.format(RE_EMAIL))
        return re_notifier.findall(mail['From'])[0]

    def get_spam_spoofed_addr(self, mail):
        re_spam_spoofed_addr = re.compile(r'(^|\n)From: .+? <({})>\n'.format(
            RE_EMAIL), re.DOTALL)
        return re_spam_spoofed_addr.findall(mail)[0][1]
    
    def get_spam_subject(self, mail):
        re_spam_subject = re.compile(r'\nSubject: [\n ]?(.+)\n')
        spam_subject = decode_header(re_spam_subject.findall(mail)[0])[0]
        try:
            return spam_subject[0].decode(spam_subject[1])
        except AttributeError:
            return spam_subject[0]
    
    def get_spam_sender(self, mail):
        re_spam_received = r'R?eceived: (from|by) (.+?)\n[A-Z]'
        re_spam_references = r'R?eferences: (.+?)\n[A-Z]'
        re_data = r'({}|{}|{})'.format(RE_DOMAIN, RE_EMAIL, RE_IPV4)
        spam_sender = []
        for match in re.findall(re_spam_received, mail, re.DOTALL):
            for data in re.findall(re_data, match[1]):
                if not (re.match(RE_IPV4_PRIVATE,data[0]) or 
                    re.match(RE_DOMAIN_SELF,data[0])):
                    spam_sender.append(data[0])
        if not spam_sender:
            for match in re.findall(re_spam_references, mail, re.DOTALL):
                for data in re.findall(re_data, match[1]):
                    if not (re.match(RE_IPV4_PRIVATE,data[0]) or 
                        re.match(RE_DOMAIN_SELF,data[0])):
                        spam_sender.append(data[0])
        return list(set(spam_sender))  # remove duplicates
    
    def logger(self, notifier_addr, spam_spoofed_addr, spam_subject, 
        spam_sender):
        logpattern = f'notifier_addr="{notifier_addr}",spam_spoofed_addr="{spam_spoofed_addr}",spam_subject="{spam_subject}",spam_sender="'
        try:
            logpattern += f'{";".join(spam_sender)}"'
            print(logpattern)
        except TypeError:
            logpattern += f'-"'
            print(logpattern)

    def move_mail(self, uid):
        self.imap.server.uid('COPY', uid, self.imap.bkpbox)
        self.imap.server.uid('STORE', uid, '+FLAGS', r'(\Deleted)')
        self.imap.server.expunge()
    
    def bkpclean(self):
        for uid in self.imap.server.uid('SEARCH','ALL')[1][0].split():
            self.imap.server.uid('STORE', uid, '+FLAGS', r'(\Deleted)')
            self.imap.server.expunge()
    
    def parse(self):
        for uid in self.imap.server.uid('SEARCH','ALL')[1][0].split():
            sts,data = self.imap.server.uid('FETCH', uid, '(RFC822)')
            current = message_from_bytes(data[0][1])
            notifier_addr = self.get_notifier_addr(current)
            spam_spoofed_addr = ''
            spam_subject = ''
            spam_sender = None
            if current.is_multipart():
                for part in current.walk():
                    if part.get_content_type() == 'message/rfc822':
                        attach = part.as_string()
                        spam_spoofed_addr = self.get_spam_spoofed_addr(attach)
                        spam_subject = self.get_spam_subject(attach)
                        spam_sender = self.get_spam_sender(attach)
            self.move_mail(uid)
            self.logger(notifier_addr, spam_spoofed_addr, spam_subject,
                spam_sender)
