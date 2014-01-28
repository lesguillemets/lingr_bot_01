#!/usr/bin/env python
# encoding:utf-8

import urllib2 as ul

def nicodic(articlename):
    url = 'http://dic.nicovideo.jp/a/' + ul.quote(articlename)
    return url
