#!/usr/bin/python
# encoding:utf-8
import urllib2 as ul

def pyref(library_name, version='2'):
    try:
        req = ul.Request("http://docs.python.org/{}/library/{}".format(
            version, library_name))
        req.get_method = lambda : 'HEAD'
        U = ul.urlopen(req)
        if U.getcode() == 200:
            return "http://docs.python.org/{}/library/{}".format(
                version, library_name)
        else:
            return "Got code {}".format(U.getcode())
    except ul.HTTPError:
            return "Not Found."

def pyref3(library_name):
    return pyref(library_name, version='3')
