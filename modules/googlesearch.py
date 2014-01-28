#!/usr/bin/python
# encoding:utf-8
import urllib2 as ul

def gslink(qu):  # google search
    
    if isinstance(qu, str) or isinstance(qu, unicode):
        queries = qu.split()
    elif isinstance(qu, list) or isinstance(qu, tuple):
        queries = qu
    else:
        raise ValueError, "Should be list, tuple or string/unicode."
    
    return "https://google.com/search?q={}".format(
        '+'.join([ul.quote(q.encode('utf-8')) for q in queries]))

def gslink_img(qu):  # google image search
    
    if isinstance(qu, str) or isinstance(qu, unicode):
        queries = qu.split()
    elif isinstance(qu, list) or isinstance(qu, tuple):
        queries = qu
    else:
        raise ValueError, "Should be list, tuple or string/unicode."
    
    return "https://google.com/search?tbm=isch&q={}".format(
        '+'.join([ul.quote(q.encode('utf-8')) for q in queries]))


if __name__ == '__main__':
    print gslink_img(u'あ い')
