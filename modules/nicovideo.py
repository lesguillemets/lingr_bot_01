#!/usr/bin/env python2
# coding:utf-8

import json
import urllib2

DATA = {
    'query': '',
    'service': [
        'video'
    ],
    'search' : ['title', 'tags'],
    'join' : [
        'cmsid','title'
    ],
    'filters': [],
    'sort_by': 'view_counter',
    'order' : 'desc',
    'reason' : 'user',
    'size' : 1,
    'from' : 0
}

def nico_topsearch(title):
    data = dict(DATA, query=title.encode("utf-8"))
    req = urllib2.Request('http://api.search.nicovideo.jp/api/',
                          data=json.dumps(data),
                          headers = {
                            'Content-Type' : 'application/json'
                          })
    response = urllib2.urlopen(req).readlines()
    try:
        videodata = json.loads(response[2])['values'][0]
        return videodata
    except KeyError:
        return None

def nico_topvideo(title):
    videodata = nico_topsearch(title)
    if videodata:
        return ("{}\nhttp://www.nicovideo.jp/watch/{}".format(
            videodata['title'].encode('utf-8'), videodata['cmsid']))
    else:
        return "No match found."

def responsechecker(title):
    data = dict(DATA, query=title.encode("utf-8"))
    req = urllib2.Request('http://api.search.nicovideo.jp/api/',
                          data=json.dumps(data),
                          headers = {
                            'Content-Type' : 'application/json'
                          })
    response = urllib2.urlopen(req)
    print(response.read())

if __name__ == '__main__':
    videodata = (nico_topsearch(u"ミク"))
    print("{}\nhttp://www.nicovideo.jp/watch/{}".format(
        videodata['title'].encode('utf-8'),videodata['cmsid']))
