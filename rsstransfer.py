#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import glob
from urllib2 import urlopen, Request
from urllib import urlencode
import getpass

LOGIN_URL = 'https://www.google.com/accounts/ClientLogin'
TOKEN_URL= 'https://www.google.com/reader/api/0/token'

def get_auth_header(mail):
    """client login to get authorization header"""
    pwd = getpass.getpass()
    request = Request(LOGIN_URL, urlencode({
        'service': 'reader',
        'Email': mail,
        'Passwd': pwd,
        'source': 'mbp'
        }))
    try:
        ret = urlopen(request)
    except:
        print  'auth failed'
        sys.exit(-1)

    auth = ret.read().split()[2][5:]
    return {'Authorization': 'GoogleLogin auth=' + auth}


def get_token(header):
    """docstring for get_token"""
    request = Request(TOKEN_URL, headers=header)
    try:
        ret = urlopen(request)
        return ret.read()
    except:
        print 'get token failed'
        sys.exit(-1)

def add_feed(token, header, feedurl):
    """docstring for add rss list"""
    request = Request('https://www.google.com/reader/api/0/subscription/quickadd?output=json', urlencode({
        'quickadd': feedurl,
        'T': token
        }), headers=header)
    try:
        ret = urlopen(request)
        ret.read()
    except :
        print 'add feed failed'
        sys.exit(-1)

def list_mail_feeds():
    """list all existed rss feeds from mail"""
    path = '~/Library/Mail/V2/RSS/*/Info.plist'
    plist =  glob.glob(os.path.expanduser(path))
    list = []
    for file in plist:
        flag = False
        for line in open(file):
            if flag:
                #<string>http://somemory.com/myblog/rss.php</string>
                list.append(line[9:-10])
                break
            if 'Feed' in line:
                flag = True
    return list


def usage():
    """print usage"""
    print '-' * 20
    print 'python rsstranfer.py your_google_email'
    print '-' * 20

def main():
    """main entry"""
    if len(sys.argv) < 2:
        usage()
        sys.exit(-1)
    header = get_auth_header(sys.argv[1])
    token = get_token(header)
    feed_list = list_mail_feeds()
    print 'found %d feeds:\n' % (len(feed_list))
    for feed in feed_list:
        print '%s' % feed
        add_feed(token, header,feed)

if __name__ == "__main__":
    main()
